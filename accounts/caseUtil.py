import datetime
from rest_framework import mixins, status
import pytz
from accounts.constants import ActionTypes, CaseStatus, UserRole
from accounts.dateUtils import working_days
from accounts.models import AuditLog, BaseUserModel, Case, UserRoleFactory
from django.db.models.query import QuerySet
from accounts.utils import current_time

def merge_case(fromuser,fromRole,touser,cases,userRole):
    if  not touser: 
        return {'errorMessage':"Please pass the required params"},status.HTTP_400_BAD_REQUEST
    if int(touser)<0:
        return {'errorMessage':"Negative value is not supported"},status.HTTP_400_BAD_REQUEST
    try:
        toRole=UserRoleFactory.objects.get(id=touser,is_active=True)
    except UserRoleFactory.DoesNotExist:
        return {"errorMessage": "Role with ID {} doesn't exist".format(touser)},status.HTTP_404_NOT_FOUND
        
    if fromuser == touser:
        return {"errorMessage": "The emails of both user should not be same"},status.HTTP_403_FORBIDDEN
        
    if fromRole.role.role!=toRole.role.role:
        return {"errorMessage": "The roles of both user should be same"},status.HTTP_403_FORBIDDEN
    if fromRole.factory_fk!=toRole.factory_fk:
        return {"errorMessage": "Both Users should belong to same Factory"},status.HTTP_403_FORBIDDEN
    #can update these cases at a one go using dynamic qureysets
    transfer_cases(toRole,fromRole,cases,userRole,ActionTypes.CASE_TRANSFERED_MERGE)
    fromRole.is_active=False
    fromRole.save()
    
    message = {"message": "Cases from user {} are assigned to user {} ".format(fromRole.user_fk.user_name,toRole.user_fk.user_name),"statusCode":"cases_merged"}
    return message,status.HTTP_200_OK
def split_cases(fromRole,request,cases,userRole):
    remainingUserRoles=UserRoleFactory.objects.filter(role=fromRole.role,is_active=True,user_fk__is_active=True,user_fk__company_fk=fromRole.user_fk.company_fk,factory_fk=fromRole.factory_fk) 
    if(remainingUserRoles.count()<=1):

        return {"errorMessage": "Can’t split cases from user {} :There is only one User of role {} in this factory".format(
                        fromRole.user_fk.user_name,fromRole.role.role),"statusCode":"cases_not_split_only_one_user"
                },status.HTTP_403_FORBIDDEN

    if fromRole.role.role==UserRole.CASE_REPORTER:
        cases=Case.objects.filter(CaseReporter=fromRole).exclude(CaseStatus__in=[CaseStatus.CLOSED,CaseStatus.COMPLETED])
        company=fromRole.user_fk.company_fk
        factory=fromRole.factory_fk
        crs=UserRoleFactory.objects.filter(role__role=UserRole.CASE_REPORTER,user_fk__company_fk=company,factory_fk=factory,is_active=True).exclude(id=fromRole.id)
        splitcases(request,cases,crs,fromRole.role.role,userRole,fromRole)
    if fromRole.role.role==UserRole.CASE_MANAGER:
        cases=Case.objects.filter(CaseManager=fromRole).exclude(CaseStatus__in=[CaseStatus.CLOSED,CaseStatus.COMPLETED])
        company=fromRole.user_fk.company_fk
        factory=fromRole.factory_fk
        cms=UserRoleFactory.objects.filter(role__role=UserRole.CASE_MANAGER,user_fk__company_fk=company,factory_fk=factory,is_active=True).exclude(id=fromRole.id)
        splitcases(request,cases,cms,fromRole.role.role,userRole,fromRole)
    if fromRole.role.role==UserRole.CASE_TROUBLESHOOTER:
        cases=Case.objects.filter(CaseTroubleShooter=fromRole).exclude(CaseStatus__in=[CaseStatus.CLOSED,CaseStatus.COMPLETED])
        company=fromRole.user_fk.company_fk
        factory=fromRole.factory_fk
        cts=UserRoleFactory.objects.filter(role__role=UserRole.CASE_TROUBLESHOOTER,user_fk__company_fk=company,factory_fk=factory,is_active=True).exclude(id=fromRole.id)
        splitcases(request,cases,cts,fromRole.role.role,userRole,fromRole)
    if fromRole.role.role==UserRole.REGIONAL_ADMIN:
        cases=Case.objects.filter(RegionalAdmin=fromRole).exclude(CaseStatus__in=[CaseStatus.CLOSED,CaseStatus.COMPLETED])
        company=fromRole.user_fk.company_fk
        region=fromRole.region_fk
        ras=UserRoleFactory.objects.filter(role__role=UserRole.REGIONAL_ADMIN,user_fk__company_fk=company,region_fk=region,is_active=True).exclude(id=fromRole.id)
        splitcases(request,cases,ras,fromRole.role.role,userRole,fromRole)
    fromRole.is_active=False
    fromRole.save()
    
    message = {
            "message": "Cases from user {} are split equally among users of the same role ".format(
                fromRole.user_fk.user_name),"statusCode":"cases_splited"}
    return message,status.HTTP_200_OK
def assign_cases(touser,fromRole,cases,userRole):
    if  not touser:
        return {'errorMessage':"Please pass the required params"},status.HTTP_400_BAD_REQUEST
    try:
        toRole=BaseUserModel.objects.get(email=touser,is_active=True)
    except BaseUserModel.DoesNotExist:
        return {
                "errorMessage": "User with Email ID {} doesn't exist".format(toRole
                                                                             )},status.HTTP_404_NOT_FOUND
        
    if fromRole.user_fk.id == toRole.id:
        return{"errorMessage": "The emails of both user should not be same"},status.HTTP_403_FORBIDDEN
    if fromRole.user_fk.company_fk!=toRole.company_fk:
        return {"errorMessage": "Both Users should belong to same Company"},status.HTTP_403_FORBIDDEN
    print(toRole) 
    newTouserRole,createduser=UserRoleFactory.objects.get_or_create(user_fk=toRole,factory_fk=fromRole.factory_fk,role=fromRole.role)
    if createduser==False:
        if newTouserRole.is_active==False:
            newTouserRole.is_active=True
            newTouserRole.save()
    
    
    print(newTouserRole)
    permission_instances = fromRole.user_permissions.all()
    # Assign fetched permission instances to the target user
    newTouserRole.user_permissions.set(permission_instances)
    transfer_cases(newTouserRole,fromRole,cases,userRole,ActionTypes.CASE_TRANSFERED_ASSIGN)
    fromRole.is_active=False
    fromRole.save()
    
    message = {"message": "Dashboard from user {} are assigned to user {} ".format(fromRole.user_fk.user_name,newTouserRole.user_fk.user_name),"statusCode":"dashboard_assigned"}
    return message,status.HTTP_200_OK
def splitcases(request,cases,crs,role,userRole,fromRole):
    num_reporters = crs.count()
    list_num=list(range(0,num_reporters))
    i=0
    for case in cases:
        if(i>(crs.count()-1)):
            i=0
        if role==UserRole.CASE_REPORTER:
            case.CaseReporter=crs[list_num[i]]
            T0T1T2Breached(case,"T1vrfDate")
        if role==UserRole.CASE_MANAGER:
            case.CaseManager=crs[list_num[i]]
            T0T1T2Breached(case,"T1vrfDate")
        if role==UserRole.CASE_TROUBLESHOOTER:
            case.CaseTroubleShooter=crs[list_num[i]]
            if case.Complainer is not None:
                if case.CaseStatus == CaseStatus.ASSIGNED_TO_TROUBLESHOOTER:
                    T0T1T2Breached(case,"T2vrfDate")
                elif case.CaseStatus == CaseStatus.UNDER_INVESTIGATION or case.CaseStatus==CaseStatus.RE_INVESTIGATION:
                    T3Breached(case,"T3vrfDate")
            else:
                T3Breached(case,"T2vrfDate")
        auditlog = AuditLog.objects.create(
                    case=case,
                    status=case.CaseStatus,
                    created_by=userRole,
                    prev_state=fromRole.id,
                    current_state=crs[list_num[i]].id,
                    message="",
                    action_type=ActionTypes.CASE_TRANSFERED_SPLIT,
                )
        i=i+1
        
        case.save()

def transfer_cases(toRole,fromRole:UserRoleFactory,cases:QuerySet,userRole,ActionType)->None:
    
    for case in cases:
        if fromRole.role.role==UserRole.CASE_REPORTER:
            case.CaseReporter=toRole
            T0T1T2Breached(case,"T1vrfDate")
        elif fromRole.role.role==UserRole.CASE_MANAGER:
            case.CaseManager=toRole
            T0T1T2Breached(case,"T1vrfDate")
        elif fromRole.role.role==UserRole.CASE_TROUBLESHOOTER:
            case.CaseTroubleShooter=toRole
            if case.Complainer is not None:
                if case.CaseStatus == CaseStatus.ASSIGNED_TO_TROUBLESHOOTER:
                    T0T1T2Breached(case,"T2vrfDate")
                elif case.CaseStatus == CaseStatus.UNDER_INVESTIGATION or case.CaseStatus==CaseStatus.RE_INVESTIGATION:
                    T3Breached(case,"T3vrfDate")
            else:
                T3Breached(case,"T2vrfDate")
        elif fromRole.role==UserRole.REGIONAL_ADMIN:
            case.RegionalAdmin=toRole 
        auditlog = AuditLog.objects.create(
                    case=case,
                    status=case.CaseStatus,
                    created_by=userRole,
                    prev_state=fromRole.id,
                    current_state=toRole.id,
                    message="",
                    action_type=ActionType,
                )
        case.save()

def T0T1T2Breached(case,date):
    startDate = getattr(case, date)
    setattr(case, date, current_time())
    endDate = current_time()
    days = working_days(startDate, endDate, case.Factory)
    if case.Breached != True:
        if days <= 1:
            case.Breached = None
        else:
            case.Breached = True

def T3Breached(case,date):
    def Breached(time,deadline):
        if case.Breached != True:
            if time <= deadline:
                case.Breached = None
            else:
                case.Breached = True
    startDate = getattr(case, date)
    setattr(case, date, current_time())
    endDate = current_time()
    days = working_days(startDate,endDate, case.Factory)
    priorities = {"Canteen food":"Medium", "Canteen cleanliness & infrastructure":"Minor", "Factory temperature & conditions":"Medium", "Machine maintenance":"Medium", "PPE":"Minor",
            "Shop Floor cleanliness":"Minor", "Washroom cleanliness":"Minor", "Leave":"Medium", "Absenteeism":"Medium",
            "Conflict with People Officer":["Major","Level 1"], "Conflict with co-worker":["Major","Level 1"], "Welfare schemes":"Medium", "Other facilities":"Minor", "Transport":"Minor","Dormitory":"Minor",
            "PF":"Medium", "ESI":"Medium", "Full and final":"Medium", "Compensation & Benefits":"Medium", "Sexual harassment":"Major", "Case against influential managers":["Major","Level 1"],
            "Miscellaneous":"Minor", "Dispensary facilities":"Medium"}
    subcategory=case.SubCategory
    if priorities[subcategory]=="Minor":
        if case.Priority == "Minor Grievance (Internal)":
            sla = 3
            case.Breached = Breached(days,sla)
        else:  
            sla =30
            case.Breached = Breached(days,sla)
    elif priorities[subcategory] == "Medium":
        if case.Priority == "Medium Grievance (Internal)":
            sla =3
            case.Breached = Breached(days,sla)
        else:
            sla =7
            case.Breached = Breached(days,sla)
    elif priorities[subcategory][0] == "Major":
        if priorities[subcategory][1] == "Level 1":
            sla =7
            case.Breached = Breached(days,sla)
        else:
            sla =3
            case.Breached = Breached(days,sla)
    else: # posh cases will not get affected by changing ct's
        setattr(case, date, startDate)

# def Breached(time,deadline):
#     if case.Breached != True:
#         if time <= deadline:
#             return None
#         else:
#             # return True

def deleteUtil(role):
    # if role.role.role==UserRole.FACTORY_ADMIN:
    #     return Response(
    #         {
    #                 "errorMessage": "Redirecting to Add User"
                    
    #             },
    #             status=status.HTTP_406_NOT_ACCEPTABLE,
    #     )
    if role.role.role==UserRole.REGIONAL_ADMIN:
        remainingUserRoles=UserRoleFactory.objects.filter(role=role.role,is_active=True,user_fk__is_active=True,user_fk__company_fk=role.user_fk.company_fk,region_fk=role.region_fk) 
        if(remainingUserRoles.count()<=1):
            
            return {
                        "errorMessage": "Can’t Delete user {} :There is only one User of role {} in this region".format(
                            role.user_fk.user_name,role.role.role
                        )
                    }
        case = Case.objects.none()
        case=Case.objects.filter(RegionalAdmin=role,CaseStatus__in=[
                        CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN, CaseStatus.RA_INVESTIGATION,CaseStatus.RE_INVESTIGATION_RA,CaseStatus.RESOLVED])
        if case.count()>0:
                message={
                        "errorMessage": "Can’t Delete Role {} in Region {} for the User {} : The user has pending cases left. Please clear those before changing the role.".format(
                            role.role.role,role.region_fk.Name,role.user_fk.user_name
                        )
                        }
                return message  
        role.is_active=False
        role.save()
        if UserRoleFactory.objects.filter(user_fk=role.user_fk,is_active=True).exists() == False:
            role.user_fk.is_active=False
            role.user_fk.save()

        message = {
                    "message": "Role {} in Region {} for the User {} has been deleted successfully".format(
                        role.role.role,role.region_fk.Name,role.user_fk.user_name
                    )
                }
    else:
        remainingUserRoles=UserRoleFactory.objects.filter(role=role.role,is_active=True,user_fk__is_active=True,user_fk__company_fk=role.user_fk.company_fk,factory_fk=role.factory_fk) 
        # users= BaseUserModel.objects.filter(role=user.role,is_active=True,company_fk=user.company_fk,factory_fk=user.factory_fk)
        if(remainingUserRoles.count()<=1):
            
            return {
                        "errorMessage": "Can’t Delete user {} :There is only one User of role {} in this factory".format(
                            role.user_fk.user_name,role.role.role
                        )
                    }
                    
        case = Case.objects.none()

        if role.role.role!=UserRole.FACTORY_ADMIN or role.role.role!=UserRole.SUPER_ADMIN:
            if role.role.role==UserRole.CASE_REPORTER:
                case=Case.objects.filter(CaseReporter=role,CaseStatus__in=[
                        CaseStatus.ASSIGNED_TO_TROUBLESHOOTER, CaseStatus.UNDER_INVESTIGATION,CaseStatus.ASSIGNED_TO_REPORTER,CaseStatus.ASSIGNED_TO_MANAGER,CaseStatus.RESOLVED,CaseStatus.RE_INVESTIGATION])
            elif role.role.role==UserRole.CASE_MANAGER:
                case=Case.objects.filter(CaseManager=role,CaseStatus__in=[
                        CaseStatus.ASSIGNED_TO_TROUBLESHOOTER, CaseStatus.UNDER_INVESTIGATION,CaseStatus.ASSIGNED_TO_MANAGER,CaseStatus.RESOLVED,CaseStatus.RE_INVESTIGATION])
            elif role.role.role==UserRole.CASE_TROUBLESHOOTER:
                case=Case.objects.filter(CaseTroubleShooter=role,CaseStatus__in=[
                        CaseStatus.ASSIGNED_TO_TROUBLESHOOTER, CaseStatus.UNDER_INVESTIGATION,CaseStatus.RESOLVED,CaseStatus.RE_INVESTIGATION])
            print(case)
            if case.count()>0:
                message={
                        "errorMessage": "Can’t Delete Role {} in Factory {} for the User {} : The user has pending cases left. Please clear those before changing the role.".format(
                            role.role.role,role.factory_fk.Code,role.user_fk.user_name
                        )
                        }
                
                return message  
        elif role.role.role==UserRole.FACTORY_ADMIN or role.role.role==UserRole.SUPER_ADMIN:
            pass
        # user.delete()
        role.is_active=False
        role.save()
        if UserRoleFactory.objects.filter(user_fk=role.user_fk,is_active=True).exists() == False:
            role.user_fk.is_active=False
            role.user_fk.save()

        message = {
                    "message": "Role {} in Factory {} for the User {} has been deleted successfully".format(
                        role.role.role,role.factory_fk.Code,role.user_fk.user_name
                    )
                }
            
    return message
