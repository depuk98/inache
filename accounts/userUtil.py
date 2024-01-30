from accounts.constants import CaseStatus, UserRole
from accounts.errors import serialer_error
from accounts.groups import F_ADMIN, R_ADMIN, S_ADMIN, CM_group, CR_group, CT_group
from accounts.models import BaseUserModel,Case, Factory, Role, FactoryRegion, UploadedFile_S3, User_Profilepic, UserRoleFactory
from accounts.serializers import UserPermissionsSerializer, UserPostRequestSerializer, UserRolePostRequestSerializer, createuserserializer
from rest_framework import mixins, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError, transaction
from accounts.utils import current_time
NoneType = type(None)

def uservalidations(request):
    role,created=Role.objects.get_or_create(role=request.data['role'])
    if request.data['role']==UserRole.REGIONAL_ADMIN:
        rausers=UserRoleFactory.objects.filter(role=role,region_fk__id=request.data['region_fk'],user_fk__company_fk__id=request.data['company_fk'],is_active=True)
        if rausers.exists():
            for rauser in rausers:
                rauser.is_active=False
                cases=Case.objects.filter(RegionalAdmin__id=rauser.id).exclude(CaseStatus__in=[CaseStatus.CLOSED,CaseStatus.UNRESPONSIVE])
                rauser.save()
                if UserRoleFactory.objects.filter(user_fk=rauser.user_fk,is_active=True).exists() == False:
                    rauser.user_fk.is_active=False
                    rauser.user_fk.save()
                return cases

            # deablerausers
            # and transfer their cases to this ra
    if request.data['role']==UserRole.FACTORY_ADMIN:
        fausers=UserRoleFactory.objects.filter(role=role,factory_fk__id=request.data['factory_fk'],user_fk__company_fk__id=request.data['company_fk'],is_active=True)
        if fausers.exists():
            for fauser in fausers:
                fauser.is_active=False
                fauser.save()
            # deablefausers
            pass 
        
@transaction.atomic
def create_user(request):
    cases = uservalidations(request) 
    request_ser=UserPostRequestSerializer(data=request.data)
    if request_ser.is_valid():
        user_permissions_ser=UserPermissionsSerializer(data=request.data['user_permissions'])
        if user_permissions_ser.is_valid():
            serializer = createuserserializer(data=request.data,context={'request': request})
            data={}
            if serializer.is_valid():
                account = serializer.save()
                data['response'] = "Registration Successful"
                data['email'] = account.email
                data['username'] = account.user_name
            
                refresh = RefreshToken.for_user(account)
                data['token'] = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                role,created=Role.objects.get_or_create(role=request.data['role'])
                if role.role==UserRole.REGIONAL_ADMIN:
                    userRole=UserRoleFactory.objects.create(user_fk=account,role=role,region_fk=FactoryRegion.objects.get(id=request.data['region_fk']))
                    if cases is not None and cases.exists():
                        cases.update(RegionalAdmin=userRole)
                elif role.role==UserRole.SUPER_ADMIN:
                    userRole=UserRoleFactory.objects.create(user_fk=account,role=role)
                else:
                    userRole=UserRoleFactory.objects.create(user_fk=account,role=role,factory_fk=Factory.objects.get(id=request.data['factory_fk']))
                mode = "Registered"
                assign_group_permissions(request.data,userRole)
                file=UploadedFile_S3.objects.get(s3_file_path__contains="default.png")
                profile_pic=User_Profilepic.objects.create(user_id=account.id)
                profile_pic.profile_picture=file
                profile_pic.save()
                # print(creator_permissions)
                # new_group.permissions.set(creator_permissions)
                # account.groups.add(new_group)
            elif BaseUserModel.objects.filter(email=request.data['email'],is_active=False).exists():    
                account=BaseUserModel.objects.get(email=request.data['email'],is_active=False)
                if account.company_fk.id!=request.data['company_fk']:
                    return {'errorMessage':"User with this email belongs to a different company"},status.HTTP_400_BAD_REQUEST
                account.is_active=True
                account.company=request.data['company_fk']
                account.user_name = request.data['user_name']
                account.name = request.data['name']
                account.mobile_number = request.data['mobile_number']
                account.gender = request.data['gender']
                account.updated_at = current_time()
                account.save()
                data['response'] = "User has been Activated Successfully"
                data['email'] = account.email
                data['username'] = account.user_name

                refresh = RefreshToken.for_user(account)
                data['token'] = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                role,created=Role.objects.get_or_create(role=request.data['role'])
                userRole,createduser=UserRoleFactory.objects.get_or_create(user_fk=account,role=role,factory_fk=Factory.objects.get(id=request.data['factory_fk']))
                if createduser==False:
                    if userRole.is_active==False:
                        userRole.is_active=True
                        userRole.updated_at=current_time()
                        userRole.save()
                mode="Reactivated"
                assign_group_permissions(request.data,userRole)
            else:
                error_response=serialer_error(serializer.errors)
                print(error_response,"dasdsdss")

                return {'errorMessage':error_response},status.HTTP_400_BAD_REQUEST
            message = {
                        "message": "User {} for the Factory {} with role {} has been {} successfully".format(
                            account.email,account.company_fk.Legalcompanyname, userRole.role, mode
                        ),
                        "UserData":data
                    }
            return message, status.HTTP_200_OK
        else:
            error_response=serialer_error(user_permissions_ser.errors)
            print(error_response,"dasdsdss")

            return error_response,status.HTTP_400_BAD_REQUEST
    else:
        error_response=serialer_error(request_ser.errors)
        print(error_response,"dasdsdss")
        return error_response,status.HTTP_400_BAD_REQUEST
@transaction.atomic  
def create_role(request):
    try:
        user=BaseUserModel.objects.get(email=request.data['email'])
    except BaseUserModel.DoesNotExist:
        return {
                "errorMessage": "User with email {} doesn't exist".format(
                    request.data['email']
                )
            },status.HTTP_404_NOT_FOUND
    cases=uservalidations(request)
    request_ser=UserRolePostRequestSerializer(data=request.data)
    if request_ser.is_valid():
        user_permissions_ser=UserPermissionsSerializer(data=request.data['user_permissions'])
        if user_permissions_ser.is_valid():
            role,created=Role.objects.get_or_create(role=request.data['role'])
            if role.role==UserRole.REGIONAL_ADMIN:
                userRole,createduser=UserRoleFactory.objects.get_or_create(user_fk=user,role=role,region_fk=FactoryRegion.objects.get(id=request.data['region_fk']))
                if cases is not None and cases.exists():
                    cases.update(RegionalAdmin=userRole)
            else:
                userRole,createduser=UserRoleFactory.objects.get_or_create(user_fk=user,role=role,factory_fk=Factory.objects.get(id=request.data['factory_fk']))
            # userRole,createduser=UserRoleFactory.objects.get_or_create(user_fk=user,role=role,factory_fk=Factory.objects.get(id=request.data['factory_fk']))
            if createduser==False:
                if userRole.is_active==False:
                    userRole.is_active=True
                    userRole.updated_at=current_time()
                    userRole.save()
            
            assign_group_permissions(request.data,userRole)
            if role.role==UserRole.REGIONAL_ADMIN:
                message = {
                            "message": "User {} for the Region {} with role {} has been registered successfully".format(
                                user.email,userRole.region_fk.Name, userRole.role
                            ),
                            # "UserData":data
                        }
            else:
                message = {
                            "message": "User {} for the Factory {} with role {} has been registered successfully".format(
                                user.email,userRole.factory_fk.Code, userRole.role
                            ),
                            # "UserData":data
                        }
            return (message, status.HTTP_200_OK)
        else:
            error_response=serialer_error(user_permissions_ser.errors)
            return error_response,status.HTTP_400_BAD_REQUEST
    else:
        error_response=serialer_error(request_ser.errors)
        return error_response,status.HTTP_400_BAD_REQUEST
    
    
def assign_group_permissions(data:dict,userRole:UserRoleFactory):
    if(data["role"] == "SUPER_ADMIN"):
        S_ADMIN(
            data,userRole)
    elif(data["role"] == "REGIONAL_ADMIN"):
        R_ADMIN(
            data,userRole)
    elif(data["role"] == "FACTORY_ADMIN"):
        F_ADMIN(
            data,userRole)
    elif(data["role"] == "CR"):
        CR_group(
            data,userRole)
    elif(data["role"] == "CM"):
        CM_group(
            data,userRole)
    elif(data["role"] == "CT"):
        CT_group(
            data,userRole)