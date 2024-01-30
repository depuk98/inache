import json
from rest_framework.test import APIRequestFactory
from rest_framework.decorators import api_view
import requests
from rest_framework.request import Request
from django.db.models.query import QuerySet
from accounts.Utils.userRoleParser import parser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, status
from accounts.caseUtil import deleteUtil, transfer_cases
from accounts.classes.Requests import CustomRequest
from accounts.constants import ActionTypes, CaseStatus, UserRole
from accounts.errors import serialer_error
from accounts.groups import get_group_permissions
from accounts.models import AuditLog, BaseUserModel, Case, Company, Factory, Role, User_Profilepic, UserRoleFactory, FactoryRegion
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.permissions import HasGroupPermission
from accounts.serializers import (
    BaseUserModelSerializer,
    UserPermissionsSerializer,
    UserPostRequestSerializer,
    UserRoleFactorySerializer,
    UserRoleFactorySerializerAll,
    UserRolePostRequestSerializer,
    createuserserializer,
    setLanguagePreferenceSerializer,
    ChangePasswordSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError, transaction
import logging
import datetime
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission
from accounts.userUtil import assign_group_permissions, create_role, create_user
from accounts.utils import current_time


class UserAV(APIView):
    # permission_classes = [HasGroupPermission]
    required_groups = {
        "GET": ["SUPER_ADMIN", "FACTORY_ADMIN", "CR", "CT", "CM", "REGIONAL_ADMIN"],
        "PATCH":["SUPER_ADMIN", "FACTORY_ADMIN", "CR", "CT", "CM", "REGIONAL_ADMIN"],
        "POST": ["SUPER_ADMIN", "FACTORY_ADMIN","REGIONAL_ADMIN"],
        "DELETE": ["SUPER_ADMIN","REGIONAL_ADMIN"],
    }
    model = "baseusermodel"

    def get(self, request: Request) -> Response:
        logger = logging.getLogger("inache_service")
        logger.debug("Entered the uaer get api")
        if request.GET.get("id") is None and (
            request.query_params.get("operation") == "user"
            or request.query_params.get("operation") == "role"
        ):
            return Response(
                {"errorMessage": "User ID missing from params"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.query_params.get("operation") == "user":
            print("dasdsadsadsdsdsd")
            try:
                BUMDetails = BaseUserModel.objects.get(pk=request.GET.get("id"))
            except BaseUserModel.DoesNotExist:
                return Response(
                    {
                        "errorMessage": "User with ID {} doesn't exist".format(
                            request.GET.get("id")
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = BaseUserModelSerializer(BUMDetails)
            data = {"roles": {}, "userData":serializer.data, "profile_picture": None}
            # user_data = serializer.data
            try:
                profile_pic=User_Profilepic.objects.get(user_id=BUMDetails.id)
                print(profile_pic.profile_picture)
                data["userData"]["profile_picture"]=int(profile_pic.profile_picture.id)

            except User_Profilepic.DoesNotExist:
                pass
            
            roles = UserRoleFactory.objects.filter(user_fk=BUMDetails, is_active=True)
            
            del data["userData"]["role"]
            del data["userData"]["factory_fk"]
            del data["userData"]["user_permissions"]
            del data["userData"]["groups"]
            perms = []
            for role in roles:
                roleperms = {}
                perms = []
                permissions = role.user_permissions.all()
                key = str(role.role) + "_" + str(role.factory_fk)
                for perm in permissions:
                    perms.append(perm.codename)
                roleperms["user_permissions"] = perms
                roleperms["role"] = str(role.role)
                roleperms["id"] = role.id
                if role.role.role==UserRole.REGIONAL_ADMIN:
                    roleperms["region_fk"] = role.region_fk.id
                    roleperms["region"] = role.region_fk.Name
                elif role.role.role==UserRole.SUPER_ADMIN:
                    pass
                else:
                    roleperms["factory_fk"] = role.factory_fk.id
                    roleperms["Code"] = str(role.factory_fk.Code)
                    roleperms["Location"] = str(role.factory_fk.Location)
                    roleperms["region"] = role.factory_fk.region.Name
                roleobj = Role.objects.get(role=role.role.role)
                grp_permissions = get_group_permissions(roleobj.group_permissions.all())
                grp_perms = []

                if grp_permissions is not None:
                    for permission in grp_permissions:
                        grp_perms.append(permission.codename)
                else:
                    pass
                roleperms["group_permissions"] = grp_perms
                data["roles"][key] = roleperms

            message = {
                "message": "User with ID {} fetched successfully".format(
                    request.GET.get("id")
                ),
                "message_body": {"User": data["userData"], "roles": data["roles"]},
            }
            return Response(message, status=status.HTTP_200_OK)
        elif request.query_params.get("operation") == "role":
            try:
                # BUMDetails = BaseUserModel.objects.get(pk=request.GET.get("id"))
                role = UserRoleFactory.objects.get(pk=request.GET.get("id"))
            except UserRoleFactory.DoesNotExist:
                return Response(
                    {
                        "errorMessage": "User Role with ID {} doesn't exist".format(
                            request.GET.get("id")
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            # serializer = UserRoleFactorySerializerAll(role)

            data = userRoleResponse(role, operation="role")
            message = {
                "message": "User with ID {} fetched successfully".format(
                    request.GET.get("id")
                ),
                "roleData": data,
            }
            return Response(message, status=status.HTTP_200_OK)
        elif request.query_params.get("operation") == "filter":
            company = request.GET.get("company")
            factory = request.GET.get("factory")
            role = request.GET.get("role")
            if company is None or factory is None or role is None:
                return Response(
                    {"errorMessage": "Please provide all company factory and role"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                Company.objects.get(id=company)
                Factory.objects.get(id=factory)
            except Exception as e:
                return Response(
                    {"errorMessage": "Company or Factory doesn't exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            if role == UserRole.REGIONAL_ADMIN:
                roles = UserRoleFactory.objects.filter(
                    region_fk=Factory.objects.get(id=factory).region,
                    role__role=role,
                    user_fk__is_active=True,
                    is_active=True,
                    user_fk__company_fk=company,
                )
            elif role not in UserRole.values:
                return Response(
                    {"errorMessage": "Role {} doesn't exist".format(role)},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                roles = UserRoleFactory.objects.filter(
                    factory_fk=factory,
                    role__role=role,
                    user_fk__is_active=True,
                    is_active=True,
                    user_fk__company_fk=company,
                )
            data = userRoleResponse(roles, operation="role-filter")
            message = {
                "message": "{} for Company {} and Factory {} fetched successfully".format(
                    request.GET.get("role"),
                    Company.objects.get(id=company),
                    Factory.objects.get(id=factory),
                ),
                "message_body": data["users"],
            }
            return Response(message, status=status.HTTP_200_OK)
        elif request.query_params.get("operation") == "admin-list":
            print("admin")
            if self.request.user.company_fk.id != int(
                self.request.query_params.get("company")
            ):
                # print(self.request.user.company_fk.id, self.request.query_params.get('company'))
                return Response(
                    {"errorMessage": "Cannot GET users of different company"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            logger = logging.getLogger("inache_service")

            logger.debug("Entered the uaer get api")
            queryset = UserRoleFactory.objects.filter(is_active=True).exclude(
                role__role=UserRole.DEFAULT_ROLE
            )  # instead of user we will show roles

            # Get the company ID and factory ID from query parameters
            company_id = self.request.query_params.get("company")
            region_id = self.request.query_params.get("region")
            factory_id = self.request.query_params.get("factory")
            role = self.request.query_params.get("role")
            # this code block is only for returning list of users(active/inactive) ehile assign dashboard functionality
            if role:
                if company_id:
                    queryset = queryset.filter(
                        user_fk__company_fk=company_id,
                        user_fk__is_active=True,
                        factory_fk__is_active=True,
                        role__role=role,
                    )  # .order_by('-updated_at')
                if region_id:
                    queryset = queryset.filter(
                        factory_fk__region=region_id,
                        is_active=True,
                        user_fk__is_active=True,
                        factory_fk__is_active=True,
                        role__role=role,
                    )
                if factory_id:
                    queryset = queryset.filter(
                        factory_fk=factory_id,
                        is_active=True,
                        user_fk__is_active=True,
                        factory_fk__is_active=True,
                        role__role=role,
                    )  # .order_by('-updated_at')
                data = userRoleResponse(queryset, operation="admin-role-list")
                message = {
                    "message": "Users fetched successfully",
                    "message_body": data,
                }
                return Response(message, status=status.HTTP_200_OK)

            # Apply filters a company and facory to the queryset
            if company_id:
                queryset = queryset.filter(
                    user_fk__company_fk=company_id,
                    is_active=True,
                    user_fk__is_active=True,
                )  # .order_by('-updated_at')
            if region_id:
                queryset = queryset.filter(
                    factory_fk__region=region_id,
                    is_active=True,
                    user_fk__is_active=True,
                )
            if factory_id:
                queryset = queryset.filter(
                    factory_fk=factory_id, is_active=True, user_fk__is_active=True
                )  # .order_by('-updated_at')
            userRole = parser(request)
            if userRole.role.role == UserRole.SUPER_ADMIN:
                queryset = queryset.filter().exclude(
                    role__role__in=[UserRole.SUPER_ADMIN]
                )
            if userRole.role.role == UserRole.REGIONAL_ADMIN:
                queryset = queryset.filter().exclude(
                    role__role__in=[UserRole.SUPER_ADMIN, UserRole.REGIONAL_ADMIN]
                )
            if userRole.role.role == UserRole.FACTORY_ADMIN:
                queryset = queryset.filter().exclude(
                    role__role__in=[UserRole.SUPER_ADMIN, UserRole.REGIONAL_ADMIN, UserRole.FACTORY_ADMIN]
                )
            if queryset.count() == 0:
                return Response(
                    {"errorMessage": "Users doesn't exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            data = userRoleResponse(queryset, operation="user-list")
            message = {"message": "Users fetched successfully", "message_body": data}
            return Response(message, status=status.HTTP_200_OK)

        else:
            return Response(
                {"errorMessage": "Please pass valid operation"},
                status=status.HTTP_400_BAD_REQUEST,
            )


    @transaction.atomic
    def post(self, request: Request) -> Response:
        # able to  make a user belonging to one company and factory belongs to diff company NEED TO FIX THIS
        if request.data["role"]==UserRole.SUPER_ADMIN:
            pass
        elif request.data["role"]==UserRole.REGIONAL_ADMIN:
            if (request.data["company_fk"]!= FactoryRegion.objects.get(id=request.data["region_fk"]).Company.id):
                            return Response(
                {
                    "errorMessage": "Cannot make user in a region that belongs to different company"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )               
        else:
            if (request.data["company_fk"]!= Factory.objects.get(id=request.data["factory_fk"]).Company.id):
                return Response(
                    {
                        "errorMessage": "Cannot make user in a factory that belongs to different company"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if request.query_params.get("operation") == "user":
            message, response_status = create_user(request)
            return Response(message, status=response_status)
        elif request.query_params.get("operation") == "role":
            message, response_status = create_role(request)
            return Response(message, status=response_status)
        else:
            return Response(
                {"errorMessage": "Please pass a valid Operation"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request: Request) -> Response:
        if request.GET.get("id") is None:
            return Response(
                {"errorMessage": "User Role ID missing from params"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.query_params.get("operation") == "user":
            try:
                # if (self.request.user.id==request.GET.get("user")) write the logic of giving thr permission to crcmct to change theor profile pic in permissions.py
                BUMDetails = BaseUserModel.objects.get(pk=request.GET.get("id"))

            except BaseUserModel.DoesNotExist:
                return Response(
                    {
                        "errorMessage": "User with ID {} doesn't exist".format(
                            request.GET.get("id")
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            data = request.data
            userRole=parser(self.request)
            if userRole.role.role not in [UserRole.SUPER_ADMIN, UserRole.FACTORY_ADMIN]:
                data = {}
                if request.data["name"]:
                    data["name"] = request.data["name"]
                else:
                    pass
            serializer = BaseUserModelSerializer(
                BUMDetails, data=data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data = {"roles": {}, "userData": serializer.data}
                del data["userData"]["role"]
                del data["userData"]["factory_fk"]
                del data["userData"]["user_permissions"]
                del data["userData"]["groups"]
                message = {
                    "message": "User with Email {} has been updated successfully".format(
                        data["userData"]["email"]
                    ),
                    "message_body": data["userData"],
                }
                return Response(message, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.query_params.get("operation") == "role":
            user_permissions_in_request = request.data["user_permissions"]
            del request.data["user_permissions"]
            if (
                request.data["company_fk"]
                != Factory.objects.get(id=request.data["factory_fk"]).Company.id
            ):
                return Response(
                    {
                        "errorMessage": "Cannot make user in a factory that belongs to diffrent company"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                # if (self.request.user.id==request.GET.get("user")) write the logic of giving thr permission to crcmct to change theor profile pic in permissions.py
                userRole = UserRoleFactory.objects.get(pk=request.GET.get("id"))

            except UserRoleFactory.DoesNotExist:
                return Response(
                    {
                        "errorMessage": "User Role with ID {} doesn't exist".format(
                            request.GET.get("id")
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            user_permissions_ser = UserPermissionsSerializer(
                data=user_permissions_in_request
            )
            if user_permissions_ser.is_valid():
                userRole.user_permissions.clear()

                serializer = UserRoleFactorySerializer(
                    userRole, data=request.data, partial=True
                )
                if serializer.is_valid(raise_exception=True):
                    role = Role.objects.get(role=request.data["role"])
                    serializer.save()
                    userRole.role = role
                    userRole.save()
                    request.data["user_permissions"] = user_permissions_in_request
                    assign_group_permissions(request.data, userRole)
                    userRole.updated_at = current_time()
                    userRole.save()
                    # user_data=BaseUserModelSerializer(userRole.user_fk)
                    data = userRoleResponse(userRole, operation="role")
                    message = {
                        "message": "User {} for the Factory {} with role {} has been edited successfully".format(
                            userRole.user_fk.email,
                            userRole.factory_fk,
                            userRole.role.role,
                        ),
                        "roleData": data,
                    }
                    return Response(message, status=status.HTTP_201_CREATED)
                error_response = serialer_error(serializer.errors)
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
            else:
                error_response = serialer_error(user_permissions_ser.errors)
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
        response = {}
        if request.query_params.get("operation") == "user":
            try:
                user = BaseUserModel.objects.get(pk=request.GET.get("id"))
            except BaseUserModel.DoesNotExist:
                return Response(
                    {
                        "errorMessage": "User with ID {} doesn't exist".format(
                            request.GET.get("id")
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            roles = UserRoleFactory.objects.filter(user_fk=user, is_active=True)
            response = {}
            for role in roles:
                print(role)
                data = deleteUtil(role)
                response[str(role)] = data
        elif request.query_params.get("operation") == "role":
            try:
                role = UserRoleFactory.objects.get(id=request.GET.get("id"))
            except UserRoleFactory.DoesNotExist:
                return Response(
                    {
                        "errorMessage": "Role with ID {} doesn't exist".format(
                            request.GET.get("id")
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            response = deleteUtil(role)
        print(response)
        return Response(response, status=status.HTTP_200_OK)


class userInformation(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        if user.is_active == False:
            return Response(
                {"errorMessage": "User is not active"},
                status=status.HTTP_403_FORBID,
            )
        if request.query_params.get("operation") == "password":
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                old_password = serializer.data["old_password"]
                new_password = serializer.data["new_password"]
                if not user.check_password(old_password):
                    return Response(
                        {"errorMessage": "Old password does not match"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                user.set_password(new_password)
                user.save()
                return Response(
                    {
                        "message": "Password Changed successfully for User with email {} ".format(
                            user.email
                        )
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                error_response = serialer_error(serializer.errors)
                # print(error_response)
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        elif request.query_params.get("operation") == "language":
            serializer = setLanguagePreferenceSerializer(data=request.data)
            if serializer.is_valid():
                language = serializer.data["Languages"]
                user.language = language
                user.save()
                return Response(
                    {
                        "message": "Language Preferences set successfully for User with email {} ".format(
                            user.email
                        )
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                error_response = serialer_error(serializer.errors)
                # print(error_response)
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(
                "Please provide valid parameter", status=status.HTTP_400_BAD_REQUEST
            )


def userRoleResponse(queryset, operation):
    if isinstance(queryset, QuerySet) == True and operation == "role-filter":
        print("if1")
        data = {"users": {}}
        perms = []
        i = 0
        for role in queryset:
            print(role, role.role)
            roleperms = {}
            perms = []
            permissions = role.user_permissions.all()
            for perm in permissions:
                perms.append(perm.codename)
            roleperms["user_permissions"] = perms
            serializer = BaseUserModelSerializer(role.user_fk)
            roleperms["user"] = serializer.data
            del roleperms["user"]["groups"]
            del roleperms["user"]["id"]
            del roleperms["user"]["role"]
            del roleperms["user"]["factory_fk"]
            del roleperms["user"]["user_permissions"]
            roleperms["user_id"] = serializer.data["id"]
            roleperms["role"] = str(role.role)
            roleperms["role_id"] = role.id
            if role.role.role==UserRole.REGIONAL_ADMIN:
                roleperms["region_fk"] = role.region_fk.id
                roleperms["region"] = role.region_fk.Name
            elif role.role.role==UserRole.SUPER_ADMIN:
                pass
            else:
                roleperms["factory_fk"] = role.factory_fk.id
                roleperms["Code"] = str(role.factory_fk.Code)
                roleperms["Location"] = str(role.factory_fk.Location)
                roleperms["region"] = role.factory_fk.region.Name
            roleperms["updated_at"] = str(role.updated_at)
            roleobj = Role.objects.get(role=role.role.role)
            grp_permissions = get_group_permissions(roleobj.group_permissions.all())
            grp_perms = []

            if grp_permissions is not None:
                for permission in grp_permissions:
                    grp_perms.append(permission.codename)
            else:
                pass
            # This code calls the get_group_permissions function with the name of the group you want to retrieve permissions for. If the group is found, it loops through the retrieved Permission objects and prints their codename attribute. If the group is not found, it prints a message indicating that the group was not found.
            roleperms["group_permissions"] = grp_perms
            data["users"][i] = roleperms
            i = i + 1
        return data

    elif isinstance(queryset, UserRoleFactory) == True and operation == "role":
        print("if2")

        data = {}
        roleperms = {}
        perms = []
        permissions = queryset.user_permissions.all()
        key = (
            str(queryset.user_fk.email)
            + "_"
            + str(queryset.role)
            + "_"
            + str(queryset.factory_fk)
        )
        for perm in permissions:
            perms.append(perm.codename)
        serializer = BaseUserModelSerializer(queryset.user_fk)
        roleperms["user"] = serializer.data
        del roleperms["user"]["groups"]
        del roleperms["user"]["role"]
        del roleperms["user"]["factory_fk"]
        del roleperms["user"]["user_permissions"]
        roleperms["user_permissions"] = perms
        roleperms["role"] = str(queryset.role)
        roleperms["id"] = queryset.id
        if queryset.role.role==UserRole.REGIONAL_ADMIN:
            roleperms["region_fk"] = queryset.region_fk.id
            roleperms["region"] = str(queryset.region_fk.Name)
        elif queryset.role.role==UserRole.SUPER_ADMIN:
            pass
        else:
            roleperms["factory_fk"] = queryset.factory_fk.id
            roleperms["Code"] = str(queryset.factory_fk.Code)
            roleperms["Location"] = str(queryset.factory_fk.Location)
            roleperms["region"] = str(queryset.factory_fk.region.Name)
        roleobj = Role.objects.get(role=queryset.role.role)
        roleperms["updated_at"] = str(queryset.updated_at)

        grp_permissions = get_group_permissions(roleobj.group_permissions.all())
        grp_perms = []

        if grp_permissions is not None:
            for permission in grp_permissions:
                grp_perms.append(permission.codename)
        else:
            pass
        # This code calls the get_group_permissions function with the name of the group you want to retrieve permissions for. If the group is found, it loops through the retrieved Permission objects and prints their codename attribute. If the group is not found, it prints a message indicating that the group was not found.
        roleperms["group_permissions"] = grp_perms
        data[key] = roleperms
        return data
    elif isinstance(queryset, QuerySet) == True and operation == "admin-role-list":
        print("if3")

        data = {"users": {}}
        for role in queryset:
            print(role, role.role)
            roleperms = {}
            perms = []
            # permissions = role.user_permissions.all()
            # for perm in permissions:
            #     perms.append(perm.codename)
            # roleperms['user_permissions'] = (perms)
            serializer = BaseUserModelSerializer(role.user_fk)
            roleperms["user"] = serializer.data
            del roleperms["user"]["groups"]
            del roleperms["user"]["role"]
            del roleperms["user"]["factory_fk"]
            del roleperms["user"]["user_permissions"]
            del roleperms["user"]["gender"]
            del roleperms["user"]["language"]
            del roleperms["user"]["date_of_birth"]
            roleperms["role"] = str(role.role)
            roleperms["role_id"] = role.id
            if role.role.role==UserRole.REGIONAL_ADMIN:
                roleperms["region_fk"] = role.region_fk.id
                roleperms["region"] = str(role.region_fk.Name)
            elif role.role.role==UserRole.SUPER_ADMIN:
                pass
            else:
                roleperms["factory_fk"] = role.factory_fk.id
                roleperms["Code"] = str(role.factory_fk.Code)
                roleperms["Location"] = str(role.factory_fk.Location)
                roleperms["region"] = str(role.factory_fk.region.Name)
            roleperms["updated_at"] = str(role.updated_at)
            
            roleobj = Role.objects.get(role=role.role.role)
            # grp_permissions = get_group_permissions(roleobj.group_permissions.all())
            # grp_perms = []

            # if grp_permissions is not None:
            #     for permission in grp_permissions:
            #         grp_perms.append(permission.codename)
            # else:
            #     pass
            # # This code calls the get_group_permissions function with the name of the group you want to retrieve permissions for. If the group is found, it loops through the retrieved Permission objects and prints their codename attribute. If the group is not found, it prints a message indicating that the group was not found.
            # roleperms['group_permissions'] = grp_perms
            data["users"][role.user_fk.id] = roleperms
        return data
    elif isinstance(queryset, QuerySet) == True and operation == "user-list":
        data = {"users": {}}
        for role in queryset:
            perms = []
            permissions = role.user_permissions.all()
            if role.user_fk.id in data["users"]:
                if role.role.role==UserRole.REGIONAL_ADMIN:
                    userRole = {
                        "id": role.id,
                        "role": str(role.role),
                        "region_fk": role.region_fk.id,
                        'region':str(role.region_fk.Name),
                        'updated_at':str(role.updated_at)
                    }
                elif role.role.role==UserRole.SUPER_ADMIN:
                    userRole = {
                        "id": role.id,
                        "role": str(role.role),
                        'updated_at':str(role.updated_at)
                    }
                else:
                    userRole = {
                        "id": role.id,
                        "role": str(role.role),
                        "factory_fk": role.factory_fk.id,
                        "FactoryCode": str(role.factory_fk.Code),
                        "Location": str(role.factory_fk.Location),
                        'region':str(role.factory_fk.region.Name),
                        'updated_at':str(role.updated_at)
                    } 
                data["users"][role.user_fk.id]["roles"][role.id] = userRole

            else:
                rolobj = {"roles": {}}

                serializer = BaseUserModelSerializer(role.user_fk)
                rolobj["user"] = serializer.data
                del rolobj["user"]["groups"]
                del rolobj["user"]["role"]
                del rolobj["user"]["factory_fk"]
                del rolobj["user"]["user_permissions"]
                del rolobj["user"]["gender"]
                del rolobj["user"]["language"]
                del rolobj["user"]["date_of_birth"]
                if role.role.role==UserRole.REGIONAL_ADMIN:
                    userRole = {
                        "id": role.id,
                        "role": str(role.role),
                        "region_fk": role.region_fk.id,
                        'region':str(role.region_fk.Name),
                        'updated_at':str(role.updated_at)
                    }
                elif role.role.role==UserRole.SUPER_ADMIN:
                    userRole = {
                        "id": role.id,
                        "role": str(role.role),
                        'updated_at':str(role.updated_at)
                    }
                else:
                    userRole = {
                        "id": role.id,
                        "role": str(role.role),
                        "factory_fk": role.factory_fk.id,
                        "FactoryCode": str(role.factory_fk.Code),
                        "Location": str(role.factory_fk.Location),
                        'region':str(role.factory_fk.region.Name),
                        'updated_at':str(role.updated_at)
                    }      
                data["users"][role.user_fk.id] = rolobj
                data["users"][role.user_fk.id]["roles"][role.id] = userRole
        return data


class addAssignUserRoleAV(APIView):
    @transaction.atomic
    def post(self, request):
        fromRole = request.data["from"]
        try:
            fromUserRole = UserRoleFactory.objects.get(id=fromRole, is_active=True)
        except UserRoleFactory.DoesNotExist:

            return Response(
                "From user does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        toUserRole = request.data["to"]
        print(toUserRole, fromRole)
        userRole = parser(request)
        if request.query_params.get("operation") == "user":
            # api_url = 'http://localhost:8000/api/accounts/users/?operation=user'
            # response = requests.post(api_url,json=toUserRole)
            # print(response.status_code,response,"dasdsds")
            # error_data = json.loads(response.content.decode('utf-8'))
            # print(response.status_code,response.content,error_data,"dasdsds")
            custom_request = CustomRequest(toUserRole, request.user)

            response_message, response_status = create_user(custom_request)
            if response_status == 200:
                data = response_message
                arg = {
                    UserRole.CASE_REPORTER: {
                        "CaseStatus__in": [CaseStatus.ASSIGNED_TO_REPORTER],
                        "CaseReporter": fromUserRole,
                    },
                    UserRole.CASE_MANAGER: {
                        "CaseStatus__in": [CaseStatus.ASSIGNED_TO_MANAGER],
                        "CaseManager": fromUserRole,
                    },
                    UserRole.CASE_TROUBLESHOOTER: {
                        "CaseStatus__in": [
                            CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,
                            CaseStatus.UNDER_INVESTIGATION,
                            CaseStatus.RE_INVESTIGATION,
                            CaseStatus.RESOLVED,
                        ],
                        "CaseTroubleShooter": fromUserRole,
                    },
                    UserRole.REGIONAL_ADMIN: {
                        "CaseStatus__in": [
                            CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN,
                            CaseStatus.RA_INVESTIGATION,
                            CaseStatus.RE_INVESTIGATION_RA,
                            CaseStatus.RESOLVED,
                        ],
                        "RegionalAdmin": fromUserRole,
                    },
                }
                query_args = arg.get(fromUserRole.role.role)
                print(query_args)
                cases = Case.objects.filter(**query_args)
                print(
                    cases,
                    request.data["to"]["email"],
                    fromUserRole.role,
                    fromUserRole.factory_fk,
                )
                try:
                    toUserRole = UserRoleFactory.objects.get(
                        user_fk__email=request.data["to"]["email"],
                        role=fromUserRole.role,
                        factory_fk=fromUserRole.factory_fk,
                    )
                except UserRoleFactory.DoesNotExist:
                    return Response(
                        {
                            "errorMessage": "Cannot assign dashborad to different Role/Factory"
                        }
                    )
                transfer_cases(toUserRole, fromUserRole, cases, userRole, ActionTypes.CASE_TRANSFERED_ASSIGN  )
                fromUserRole.is_active = False
                fromUserRole.save()
                auditlog = AuditLog.objects.create(
                    status="User Transfered",
                    created_by=userRole,
                    prev_state=fromUserRole.id,
                    current_state=toUserRole.id,
                    message="",
                    action_type=ActionTypes.ROLE_TRANSFERED,
                )
                if UserRoleFactory.objects.filter(user_fk=fromUserRole.user_fk,is_active=True).exists() == False:
                    fromUserRole.user_fk.is_active = False
                    fromUserRole.user_fk.save()
                message = {
                    "data": data,
                    "message": "User and UserRole created and dashboard transferred to newly created userrole",
                }

                return Response(message, status=status.HTTP_200_OK)
            else:

                return Response(response_message, status=response_status)
        elif request.query_params.get("operation") == "role":
            # api_url = 'http://localhost:8000/api/accounts/users/?operation=role'

            # response = requests.post(api_url,json=toUserRole)
            # error_data = json.loads(response.content.decode('utf-8'))
            custom_request = CustomRequest(toUserRole, request.user)
            response_message, response_status = create_user(custom_request)
            if response_status == 200:
                data = response_message
                arg = {
                    UserRole.CASE_REPORTER: {
                        "CaseStatus__in": [CaseStatus.ASSIGNED_TO_REPORTER],
                        "CaseReporter": fromUserRole,
                    },
                    UserRole.CASE_MANAGER: {
                        "CaseStatus__in": [CaseStatus.ASSIGNED_TO_MANAGER],
                        "CaseManager": fromUserRole,
                    },
                    UserRole.CASE_TROUBLESHOOTER: {
                        "CaseStatus__in": [
                            CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,
                            CaseStatus.UNDER_INVESTIGATION,
                            CaseStatus.RE_INVESTIGATION,
                            CaseStatus.RESOLVED,
                        ],
                        "CaseTroubleShooter": fromUserRole,
                    },
                    UserRole.REGIONAL_ADMIN: {
                        "CaseStatus__in": [
                            CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN,
                            CaseStatus.RA_INVESTIGATION,
                            CaseStatus.RE_INVESTIGATION_RA,
                            CaseStatus.RESOLVED,
                        ],
                        "RegionalAdmin": fromUserRole,
                    },
                }
                query_args = arg.get(fromUserRole.role.role)
                print(query_args)
                cases = Case.objects.filter(**query_args)
                print(
                    cases,
                    request.data["to"]["email"],
                    fromUserRole.role,
                    fromUserRole.factory_fk,
                )
                try:
                    toUserRole = UserRoleFactory.objects.get(
                        user_fk__email=request.data["to"]["email"],
                        role=fromUserRole.role,
                        factory_fk=fromUserRole.factory_fk,
                    )
                except UserRoleFactory.DoesNotExist:
                    return Response(
                        {
                            "errorMessage": "Cannot assign dashborad to different Role/Factory"
                        }
                    )
                transfer_cases(toUserRole, fromUserRole, cases, userRole, ActionTypes.CASE_TRANSFERED_ASSIGN)
                fromUserRole.is_active = False
                fromUserRole.save()

                auditlog = AuditLog.objects.create(
                    status="User Transfered",
                    created_by=userRole,
                    prev_state=fromUserRole.id,
                    current_state=toUserRole.id,
                    message="",
                    action_type=ActionTypes.ROLE_TRANSFERED,
                )
                if UserRoleFactory.objects.filter(user_fk=fromUserRole.user_fk,is_active=True).exists() == False:
                    fromUserRole.user_fk.is_active = False
                    fromUserRole.user_fk.save()
                message = {
                    "data": data,
                    "message": "UserRole created and dashboard transferred to newly created userrole",
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                return Response(response_message, status=response_status)


#TODO: Remove this function
@api_view(["GET"])
def sanitiseNames(request):
    users=BaseUserModel.objects.all()
    for user in users:
        if user.name is None:
            user.name=user.user_name
            user.save()
    return Response("Names filled")


#TODO: Remove this function
@api_view(["GET"])
def sanitiseInactiveUsers(request):
    users=BaseUserModel.objects.all()
    for user in users:
        if UserRoleFactory.objects.filter(user_fk=user.id,is_active=True).exists() == False:
            user.is_active = False
            user.save()
    return Response("Users with No Roles made Inactive")


#TODO: Remove this function
@api_view(["GET"])
def sanitisePoshSpecialCases(request):
    cases=Case.objects.filter(CaseCategory__in=["POSH","Special Cases"],CaseStatus__in=[CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN,CaseStatus.RA_INVESTIGATION,CaseStatus.RE_INVESTIGATION_RA,CaseStatus.RESOLVED])
    for case in cases:
        if case.RegionalAdmin:
            if case.RegionalAdmin.is_active == False:
                case.RegionalAdmin=UserRoleFactory.objects.get(role__role=UserRole.REGIONAL_ADMIN,region_fk=case.Factory.region,is_active=True)
                case.save()
    return Response("Posh and Special cases with inactive RA reassigned")


#TODO: Remove this function
@api_view(["GET"])  
def sanitiseIncentivePerms(request):
    roles = UserRoleFactory.objects.all().exclude(user_fk__company_fk__Legalcompanyname="Shahi Exports PVT LTD")
    for role in roles:
        permissions = role.user_permissions.all()
        if permissions.filter(codename="view_incentives").exists() == False:
            role.user_permissions.add(Permission.objects.get(codename="view_incentives", content_type__app_label='accounts', content_type__model='incentivepermission'))
            role.save()
    return Response("Users apart from Shahi Exports given incentive permissions")
    
    
#TODO: Need to remove this
@api_view(["GET"])
def disableFAs(request):
    users = UserRoleFactory.objects.filter(role__role=UserRole.FACTORY_ADMIN, is_active=True, user_fk__company_fk__Legalcompanyname="Shahi Exports PVT LTD")
    for user in users:
        user.is_active = False
        user.save()

    return Response("success, FA's for Shahi Company disabled")
