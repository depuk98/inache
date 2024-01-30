import datetime
from accounts.constants import ReportingMedium, UserRole, CaseStatus, CaseType, CaseActiveStatus
from accounts.models import  Case, Incentives, Role
from django.utils.timezone import localtime
from rest_framework import  status
import pytz
from datetime import  timedelta, date
from calendar import SATURDAY
from accounts.dateUtils import working_days, workingDaysAddition, count_working_hours, workingHoursAddition
from rest_framework.request import Request
from accounts.utils import current_time
class CasesService:
    def __init__(self:Request, company_id, factory_id:int):
        self.company_id = company_id
        self.factory_id = factory_id

    def getCases(self:Request, user_id:int, user_role:Role, case_type:str, critical:str):
        # print(user_id,user_role,case_type)
        if case_type == CaseType.NEW_CASES:
            cases = self._get_new_cases(user_id, user_role)
        elif case_type == CaseType.IN_PROGRESS_CASES:
            cases = self._get_in_progress_cases(user_id, user_role)
        elif case_type == CaseType.RESOLVED_CASES:
            cases = self._get_resolved_cases(user_id, user_role)
        elif case_type == CaseType.CLOSED_CASES:
         
            if critical == "true":
              
                cases = self._get_critical_closed_cases(user_id, user_role)
            else:
               
                cases = self._get_closed_cases(user_id, user_role)
        elif case_type == CaseType.APPROVED_CASES:
            cases = self._get_approved_cases(user_id, user_role)
        cases=sanitize_complainer_data(cases)
        return cases

    def _get_new_cases(self:Request, user_id:int, user_role:Role):
        unsorted_new_cases_response_body = None
        if user_role == UserRole.CASE_REPORTER:
            unsorted_new_cases_response_body = list(Case.objects.filter(
                Company=self.company_id,
                Factory=self.factory_id,
                CaseReporter=user_id,
                CaseStatus__in=[CaseStatus.ASSIGNED_TO_REPORTER]
            ).values(
                "id",
                "CaseNumber",
                "ReportingMedium",
                "Date",
                "CurrentStatus",
                "Complainer__Registered",
                "reopened"
            ))
            new_cases_response_body= sorted(unsorted_new_cases_response_body, key=lambda x: x['Date'], reverse=True)
            #update those only those cases which were new_case
            Case.objects.filter(
                Company=self.company_id, Factory=self.factory_id, CaseReporter=user_id,
                CaseStatus__in=[CaseStatus.ASSIGNED_TO_REPORTER],
                CurrentStatus=CaseActiveStatus.NEW_CASE
            ).update(CurrentStatus=CaseActiveStatus.UNREAD)
            # return new_cases_response_body
        elif user_role == UserRole.CASE_MANAGER:
            unsorted_new_cases_response_body = list(Case.objects.filter(
                Company=self.company_id, Factory=self.factory_id, CaseManager=user_id,
                CaseStatus__in=[CaseStatus.ASSIGNED_TO_MANAGER]
            ).values(
                "id",
                "CaseNumber",
                "ReportingMedium",
                "Date",
                "CaseCategory",
                "SubCategory",
                "Priority",
                "CaseReporter__user_fk__user_name",
                "CurrentStatus",
                "Complainer__Registered",
                "reopened"
            ))
            new_cases_response_body= sorted(unsorted_new_cases_response_body, key=lambda x: x['Date'], reverse=True)
            Case.objects.filter(
                Company=self.company_id, Factory=self.factory_id, CaseManager=user_id,
                CaseStatus__in=[CaseStatus.ASSIGNED_TO_MANAGER],
                CurrentStatus=CaseActiveStatus.NEW_CASE
            ).update(CurrentStatus=CaseActiveStatus.UNREAD)
            # return new_cases_response_body
        elif user_role == UserRole.CASE_TROUBLESHOOTER:
            unsorted_new_cases_response_body = list(Case.objects.filter(
                Company=self.company_id, Factory=self.factory_id, CaseTroubleShooter=user_id,
                CaseStatus__in=[CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,CaseStatus.UNDER_INVESTIGATION,CaseStatus.RE_INVESTIGATION],

            ).values(
                "id",
                "CaseNumber",
                "ReportingMedium",
                "CaseStatus",
                "Date",
                "CaseCategory",
                "SubCategory",
                "Priority",
                "CaseManager__user_fk__user_name",
                "CurrentStatus",
                "Complainer__Registered",
                "reopened"
                
            ))
            new_cases_response_body= sorted(unsorted_new_cases_response_body, key=lambda x: x['Date'], reverse=True)
            Case.objects.filter(
                Company=self.company_id, Factory=self.factory_id, CaseTroubleShooter=user_id,
                CaseStatus__in=[CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,CaseStatus.UNDER_INVESTIGATION,CaseStatus.RE_INVESTIGATION],
                CurrentStatus=CaseActiveStatus.NEW_CASE
            ).update(CurrentStatus=CaseActiveStatus.UNREAD)
        elif user_role == UserRole.REGIONAL_ADMIN:
            unsorted_new_cases_response_body = list(Case.objects.filter(
                Company=self.company_id, RegionalAdmin=user_id,
                CaseStatus__in=[CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN,CaseStatus.RA_INVESTIGATION,CaseStatus.RE_INVESTIGATION_RA]
            ).values(
                "id",
                "CaseNumber",
                "ReportingMedium",
                "Date",
                "CaseCategory",
                "SubCategory",
                "Priority",
                "Factory__Code",
                "CurrentStatus",
                "Complainer__Registered",
                "reopened"
            ))
            new_cases_response_body= sorted(unsorted_new_cases_response_body, key=lambda x: x['Date'], reverse=True)
            
            Case.objects.filter(
                Company=self.company_id, RegionalAdmin=user_id,
                CaseStatus__in=[CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN, CaseStatus.RA_INVESTIGATION,CaseStatus.RE_INVESTIGATION_RA],
                CurrentStatus=CaseActiveStatus.NEW_CASE
            ).update(CurrentStatus=CaseActiveStatus.UNREAD)
        print(new_cases_response_body)
        cases=dueDate(new_cases_response_body,user_role)
        # print(new_cases_response_body)
        return cases

    def _get_in_progress_cases(self:Request, user_id:int, user_role:Role):
        # print("dasdsa")
        query_params = {
            UserRole.CASE_REPORTER: {
                'CaseReporter': user_id,
                'CaseStatus__in': [
                    CaseStatus.ASSIGNED_TO_MANAGER,
                    CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,
                    CaseStatus.UNDER_INVESTIGATION,
                    CaseStatus.RE_INVESTIGATION,
                    CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN,
                    CaseStatus.RA_INVESTIGATION,
                    CaseStatus.RE_INVESTIGATION_RA,
                ],
            },
            UserRole.CASE_MANAGER: {
                'CaseManager': user_id,
                'CaseStatus__in': [
                    CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,
                    CaseStatus.UNDER_INVESTIGATION,
                    CaseStatus.RE_INVESTIGATION
                ],
            },
            UserRole.CASE_TROUBLESHOOTER: {
                'CaseTroubleShooter': user_id,
                'CaseStatus': str(CaseStatus.UNDER_INVESTIGATION),
            },
            UserRole.SUPER_ADMIN: {
                'CaseStatus__in': [
                    CaseStatus.ASSIGNED_TO_REPORTER,
                    CaseStatus.ASSIGNED_TO_MANAGER,
                    CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,
                    CaseStatus.UNDER_INVESTIGATION,
                    CaseStatus.RESOLVED,
                    CaseStatus.RE_INVESTIGATION,
                    CaseStatus.ASSIGNED_TO_QUALITY_CHECKER,
                ],
            },
            UserRole.FACTORY_ADMIN: {
                'CaseStatus__in': [
                    CaseStatus.ASSIGNED_TO_REPORTER,
                    CaseStatus.ASSIGNED_TO_MANAGER,
                    CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,
                    CaseStatus.UNDER_INVESTIGATION,
                    CaseStatus.RESOLVED,
                    CaseStatus.RE_INVESTIGATION,
                    CaseStatus.ASSIGNED_TO_QUALITY_CHECKER,
                ],
            },
            UserRole.REGIONAL_ADMIN: {
                'CaseStatus__in': [
                    CaseStatus.ASSIGNED_TO_REPORTER,
                    CaseStatus.ASSIGNED_TO_MANAGER,
                    CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,
                    CaseStatus.UNDER_INVESTIGATION,
                    CaseStatus.RESOLVED,
                    CaseStatus.RE_INVESTIGATION,
                    CaseStatus.ASSIGNED_TO_QUALITY_CHECKER,
                ],
            },
        }
        query_kwargs = query_params.get(user_role, {})
        query_kwargs.update({
            'Company': self.company_id,
            'Factory': self.factory_id,
        })

        if user_role == UserRole.SUPER_ADMIN or user_role == UserRole.FACTORY_ADMIN or user_role == UserRole.REGIONAL_ADMIN:
            values = getinprogress(user_role)
            cases = Case.objects.filter(**query_kwargs).values(
            *values
        ).order_by("-Date")
            cases=dueDate(cases,user_role)
        else:
            values = getvalues(user_role)
            cases = Case.objects.filter(**query_kwargs).values(
            *values
        ).order_by("-Date")

        return cases

    def _get_resolved_cases(self:Request, user_id:int, user_role:Role):

        if user_role == UserRole.CASE_REPORTER:
            user_kwargs = {'CaseReporter': user_id,'Factory':self.factory_id}
            values = getvalues(user_role)

        elif user_role == UserRole.CASE_MANAGER:
            user_kwargs = {'CaseManager': user_id,'Factory':self.factory_id}
            values = getvalues(user_role)

        elif user_role == UserRole.CASE_TROUBLESHOOTER:
            user_kwargs = {'CaseTroubleShooter': user_id,'Factory':self.factory_id}
            values = getvalues(user_role)

        elif user_role == UserRole.REGIONAL_ADMIN:
            user_kwargs = {'RegionalAdmin': user_id}
            values = getvalues(user_role)

        query = Case.objects.filter(
            **user_kwargs,
            Company=self.company_id,
            CaseStatus=CaseStatus.RESOLVED
        ).values(
            *values
        ).order_by("-Date")

        return query

    def _get_closed_cases(self:Request, user_id:int, user_role:Role):
        if user_role == UserRole.CASE_REPORTER:
            user_kwargs = {'CaseReporter': user_id}
            values = getvalues(user_role)

        elif user_role == UserRole.CASE_MANAGER:
            user_kwargs = {'CaseManager': user_id,}
            values = getvalues(user_role)

        elif user_role == UserRole.CASE_TROUBLESHOOTER:
            user_kwargs = {'CaseTroubleShooter': user_id}
            values = getvalues(user_role)

        elif user_role == UserRole.SUPER_ADMIN:
            user_kwargs = {}
            values = getvalues(user_role)

        elif user_role == UserRole.FACTORY_ADMIN:
            user_kwargs = {}
            values = getvalues(user_role)

        elif user_role == UserRole.REGIONAL_ADMIN:
            user_kwargs = {}
            values = getvalues(user_role)

        query = Case.objects.filter(
            **user_kwargs,
            Company=self.company_id,
            Factory=self.factory_id,
            CaseStatus__in=[CaseStatus.CLOSED,CaseStatus.UNRESPONSIVE]
        ).values(
            *values
        ).order_by("-Date")

        return query

    def _get_critical_closed_cases(self:Request, user_id:int, user_role:Role):

        if user_role == UserRole.REGIONAL_ADMIN:
            user_kwargs = {'RegionalAdmin': user_id}
            values = getclosed(user_role)

        query = Case.objects.filter(
            **user_kwargs,
            Company=self.company_id,
            CaseStatus__in=[CaseStatus.CLOSED,CaseStatus.UNRESPONSIVE]
        ).values(
            *values
        ).order_by("-Date")

        return query

    def _get_approved_cases(self:Request, user_id:int, user_role:Role):

        if user_role == UserRole.SUPER_ADMIN or user_role == UserRole.FACTORY_ADMIN or user_role == UserRole.REGIONAL_ADMIN:
            user_kwargs = {}
            values = getapproved(user_role)

        query = Case.objects.filter(
            **user_kwargs,
            Company=self.company_id,
            Factory=self.factory_id,
            CaseStatus = CaseStatus.APPROVED
        ).values(
            *values
        ).order_by("-Date")
        return query



def getvalues(user_role):
    query_params = {
        UserRole.CASE_REPORTER: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "Priority",
            "CaseStatus",
            "CaseManager__user_fk__user_name",
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
        },
        UserRole.CASE_MANAGER: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "Priority",
            "CaseStatus",
            "CaseReporter__user_fk__user_name",
            "CaseTroubleShooter__user_fk__user_name",
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
            },
        UserRole.CASE_TROUBLESHOOTER: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "Priority",
            "CaseStatus",
            "CaseManager__user_fk__user_name",
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
        },
        UserRole.SUPER_ADMIN: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "ClosingTime",
            "Priority",
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
        },
        UserRole.FACTORY_ADMIN: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "ClosingTime",
            "Priority",
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
        },
         UserRole.REGIONAL_ADMIN: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "Priority",
            "ClosingTime",
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
        }
    }
    
    return query_params.get(user_role, {})

# make new cmservice class for this

def getinprogress(user_role):
    query_params = {
        UserRole.SUPER_ADMIN: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "Priority",
            "CaseStatus",
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
        },
        UserRole.FACTORY_ADMIN: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "Priority",
            "CaseStatus",
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
        },
        UserRole.REGIONAL_ADMIN: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "Priority",
            "CaseStatus",
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
        },
    }
    return query_params.get(user_role, {})

def getapproved(user_role):
    query_params = {
        UserRole.SUPER_ADMIN: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "Priority",
            #"ApprovedTime", #need to fetch from auditlogs
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
        },
        UserRole.FACTORY_ADMIN: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "Priority",
            #"ApprovedTime", #need to fetch from auditlogs
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
        },
        UserRole.REGIONAL_ADMIN: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "Priority",
            #"ApprovedTime", #need to fetch from auditlogs
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
        },
    }
    return query_params.get(user_role, {})

def getclosed(user_role):
    query_params = {
        UserRole.REGIONAL_ADMIN: {
            "id",
            "CaseNumber",
            "ReportingMedium",
            "Date",
            "CaseCategory",
            "SubCategory",
            "Priority",
            "CaseStatus",
            "Factory__Code",
            "CurrentStatus",
            "Complainer__Registered",
            "reopened"
        },
    }
    return query_params.get(user_role, {})
    
def dueDate(cases,role):
    if(role == UserRole.CASE_REPORTER):
        for case in cases:
            case_obj=Case.objects.get(pk=case['id'])

            try:
                caseFreeze = Incentives.objects.get(Case=case_obj)
                userDueDate(case,caseFreeze.CRsendDate,caseFreeze.CRreceiveDate,case_obj.T1vrfDate,1)
            except Incentives.DoesNotExist:
                pass
    if(role == UserRole.CASE_MANAGER):
        for case in cases:
            case_obj=Case.objects.get(pk=case['id'])
            try:
                caseFreeze = Incentives.objects.get(Case=case_obj)
                userDueDate(case,caseFreeze.CMsendDate,caseFreeze.CMreceiveDate,case_obj.T1vrfDate,1)
            except Incentives.DoesNotExist:
                pass
    if (role == UserRole.CASE_TROUBLESHOOTER):
        for case in cases:
            # print(case,"dsadsad")
            case_obj=Case.objects.get(pk=case['id'])
            try:
                caseFreeze = Incentives.objects.get(Case=case_obj)
                
                # if user asks for more information and waiting for reply
                if case_obj.Complainer is not None:
                    if case_obj.CaseStatus==CaseStatus.ASSIGNED_TO_TROUBLESHOOTER:
                        userDueDate(case,caseFreeze.CTsendDate,caseFreeze.CTreceiveDate,case_obj.T2vrfDate,1)

                    elif case_obj.CaseStatus==CaseStatus.UNDER_INVESTIGATION or case_obj.CaseStatus==CaseStatus.RE_INVESTIGATION:
                        days=subcategory_sla_timeline(case_obj)
                        userDueDate(case,caseFreeze.CTsendDate,caseFreeze.CTreceiveDate,case_obj.T3vrfDate,days)
                else:
                    days=subcategory_sla_timeline(case_obj)
                    userDueDate(case,caseFreeze.CTsendDate,caseFreeze.CTreceiveDate,case_obj.T2vrfDate,days)
            except Incentives.DoesNotExist:
                # print(case,"pass")
                pass
    if (role == UserRole.SUPER_ADMIN) or (role == UserRole.FACTORY_ADMIN) or (role == UserRole.REGIONAL_ADMIN):
        for case in cases:
            case_obj=Case.objects.get(pk=case['id'])
            caseFreeze = Incentives.objects.get(Case=case_obj)
            if case_obj.CaseStatus == CaseStatus.ASSIGNED_TO_REPORTER:
                userDueDate(case,caseFreeze.CRsendDate,caseFreeze.CRreceiveDate,case_obj.T1vrfDate,1)
            elif case_obj.CaseStatus == CaseStatus.ASSIGNED_TO_MANAGER:
                userDueDate(case,caseFreeze.CMsendDate,caseFreeze.CMreceiveDate,case_obj.T1vrfDate,1)
            elif case_obj.CaseStatus == CaseStatus.ASSIGNED_TO_TROUBLESHOOTER or case_obj.CaseStatus == CaseStatus.UNDER_INVESTIGATION or case_obj.CaseStatus == CaseStatus.RE_INVESTIGATION:
                ctDueDate(case,caseFreeze,case_obj)
            elif case_obj.CaseStatus == CaseStatus.RESOLVED:
                resolvedDueDate(case,case_obj)
            elif case_obj.CaseStatus == CaseStatus.ASSIGNED_TO_QUALITY_CHECKER:
                qcDueDate(case)                                         
    return cases

def userDueDate(case,sendDate,receiveDate,Date,days):
    case_obj=Case.objects.get(pk=case['id'])
    # if user asks for more information and waiting for reply
    if (sendDate is not None) and (receiveDate is None):
        case['dueDate']="Awaiting Response"
        case['dueDateType']="string"
        case['dueDateBreached']=False
    # if user received reply from worker and that reply is not from previous state
    elif (receiveDate is not None) and (receiveDate > Date):
        current = count_working_hours(localtime(Date),localtime(sendDate),case_obj.Factory)
        # if due date already passed by the time he asks for information
        if current > days * 24:
            duedate=localtime(workingDaysAddition(Date,days,case_obj.Factory))
            case['dueDate']=duedate
            case['dueDateType']="timestamp"
            case['dueDateBreached']=True
        # if message sent before due date, add the remaining time from the time when he received the information
        else:
            remains = (days * 24) - current
            duedate = localtime(workingHoursAddition(localtime(receiveDate),remains,case_obj.Factory))
            case['dueDate']=duedate
            case['dueDateType']="timestamp"
            # red(due date breached) needs to be shown 24 hrs before due date
            if current_time() > duedate - timedelta(days=1):
                case['dueDateBreached']=True
            else:
                case['dueDateBreached']=False
    # normal flow 
    else:
        duedate=localtime(workingDaysAddition(Date,days,case_obj.Factory))
        case['dueDate']=duedate
        case['dueDateType']="timestamp"
        # red(due date breached) needs to be shown 24 hrs before due date
        if current_time() > duedate - timedelta(days=1):
            case['dueDateBreached']=True
        else:
            case['dueDateBreached']=False
    return case


def ctDueDate(case,caseFreeze,case_obj):
    if case_obj.Complainer is not None:
        if case_obj.CaseStatus==CaseStatus.ASSIGNED_TO_TROUBLESHOOTER:
            userDueDate(case,caseFreeze.CTsendDate,caseFreeze.CTreceiveDate,case_obj.T2vrfDate,1)

        elif case_obj.CaseStatus==CaseStatus.UNDER_INVESTIGATION or case_obj.CaseStatus==CaseStatus.RE_INVESTIGATION:
            days=subcategory_sla_timeline(case_obj)
            userDueDate(case,caseFreeze.CTsendDate,caseFreeze.CTreceiveDate,case_obj.T3vrfDate,days)

    else:
        days=subcategory_sla_timeline(case_obj)
        userDueDate(case,caseFreeze.CTsendDate,caseFreeze.CTreceiveDate,case_obj.T2vrfDate,days)

def resolvedDueDate(case,case_obj):
    Date = case_obj.ResolveTime
    dueDate = workingDaysAddition(Date,3,case_obj.Factory)
    case['dueDate']=dueDate
    case['dueDateType']="timestamp"
    if current_time() > dueDate - timedelta(days=1):
        case['dueDateBreached']=True
    else:
        case['dueDateBreached']=False
    return case

def qcDueDate(case):
    Date = date.today().replace(day=1)
    case_obj=Case.objects.get(pk=case['id'])
    dueDate = workingDaysAddition(Date,7,case_obj.Factory)
    case['dueDate']=dueDate
    case['dueDateType']="timestamp"
    case['dueDateBreached']=False
    return case

                   
                
            
def sanitize_complainer_data(cases):
    for case in cases:
        if case['ReportingMedium'] == ReportingMedium.IN_PERSON or case['ReportingMedium'] == ReportingMedium.SUGGESTION_BOX or  case['ReportingMedium'] == ReportingMedium.WORKER_COMMITTEE:  
            case['Complainer__Registered']=False
        
    return cases
def subcategory_sla_timeline(case):
    priorities = {"Canteen food":"Medium", "Canteen cleanliness & infrastructure":"Minor", "Factory temperature & conditions":"Medium", "Machine maintenance":"Medium", "PPE":"Minor",
            "Shop Floor cleanliness":"Minor", "Washroom cleanliness":"Minor", "Leave":"Medium", "Absenteeism":"Medium",
            "Conflict with People Officer":["Major","Level 1"], "Conflict with co-worker":["Major","Level 1"], "Welfare schemes":"Medium", "Other facilities":"Minor", "Transport":"Minor","Dormitory":"Minor",
            "PF":"Medium", "ESI":"Medium", "Full and final":"Medium", "Compensation & Benefits":"Medium", "Sexual harassment":"Major", "Case against influential managers":["Major","Level 1"], 
            "Dispensary facilities":"Medium","Others":"Minor"}
    subcategory=case.SubCategory
    if priorities[subcategory]=="Minor":
        if case.Priority == "Minor Grievance (Internal)":
            sla = 3
        else:  
            sla =30
    elif priorities[subcategory] == "Medium":
        if case.Priority == "Medium Grievance (Internal)":
            sla =3
        else:
            sla =7
    elif priorities[subcategory][0] == "Major":
        if priorities[subcategory][1] == "Level 1":
            sla =7
        else:
            sla =3
    else: # posh cases will not get affected by changing ct's
        sla=90
    return sla