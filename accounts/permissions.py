import re
from InacheBackend import settings
from accounts.Utils.userRoleParser import parser
from rest_framework import permissions
from accounts.models import BaseUserModel, Case, UserRoleFactory
from accounts.constants import UserRole
from django.contrib.auth.models import Group
from rest_framework import permissions
from rest_framework import exceptions
import jwt
class isSuperAdmin:
    def has_permission(self,request,view):
        userRole=parser(request)
        if userRole is None:
            return False
        if request.user == "AnonymousUser":
            return False
        if userRole.role.role==UserRole.SUPER_ADMIN:
            return True
        else:
            return False
class AdminOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        # admin_permission = bool(request.user and request.user.role=='ADMIN')
        # print(request.user.role=='ADMIN')
        # print(request.user)
        userRole=parser(request)
        if userRole is None:
            return False
        if request.user == "AnonymousUser":
            return False
        
        if request.user and request.user.is_authenticated:
            if (
                userRole.role.role == "ADMIN"
                or request.user.is_staff == True
                or request.user.is_superuser == True
            ):
                return True
            return False
        return False

class isSAorRA:
    def has_permission(self,request,view):
        userRole=parser(request)
        if userRole is None:
            return False
        if request.user == "AnonymousUser":
            return False
        if userRole.role.role==UserRole.SUPER_ADMIN or userRole.role.role==UserRole.REGIONAL_ADMIN:
            return True
        else:
            return False


class CROnly:
    def has_permission(self, request, view):
        # admin_permission = bool(request.user and request.user.role=='ADMIN')
        # print(request.user.role=='ADMIN')
        # print(request.user)
        userRole=parser(request)
        if userRole is None:
            return False
        if request.user == "AnonymousUser":
            return False
        if request.user and request.user.is_authenticated:
            if userRole.role.role == UserRole.CASE_REPORTER:
                return True
            return False
        return False


class CMOnly:
    def has_permission(self, request, view):
        # admin_permission = bool(request.user and request.user.role=='ADMIN')
        # print(request.user.role=='ADMIN')
        # print(request.user)
        userRole=parser(request)
        if userRole is None:
                return False
        if request.user == "AnonymousUser":
            return False
        if request.user and request.user.is_authenticated:
            if userRole.role.role == UserRole.CASE_MANAGER:
                return True
            return False
        return False




class CTOnly:
    def has_permission(self, request, view):
        # admin_permission = bool(request.user and request.user.role=='ADMIN')
        # print(request.user.role=='ADMIN')
        # print(request.user)
        userRole=parser(request)
        if userRole is None:
            return False
        if request.user == "AnonymousUser":
            return False
        if request.user and request.user.is_authenticated:
            if userRole.role.role == UserRole.CASE_TROUBLESHOOTER:
                return True
            return False
        return False


class FAOnly:
    def has_permission(self, request, view):
        # admin_permission = bool(request.user and request.user.role=='ADMIN')
        # print(request.user.role=='ADMIN')
        # print(request.user)
        userRole=parser(request)
        if userRole is None:
            return False
        if request.user == "AnonymousUser":
            return False
        if request.user and request.user.is_authenticated:
            if userRole.role.role == "FACTORY_ADMIN":
                return True
            return False
        return False


class is_same_company_user:
    def has_permission(self, request, view):
        # admin_permission = bool(request.user and request.user.role=='ADMIN')
        # print(request.user.role=='ADMIN')
        # print(request.user.role)
        if request.user == "AnonymousUser":
            return False
        if request.user and request.user.is_authenticated:
            if view.kwargs.get('companyId') is not None and request.user.company_fk.id == int(view.kwargs['companyId']):
                return True
            elif view.kwargs.get('caseId') is not None and request.user.company_fk.id== Case.objects.get(
                    id=view.kwargs["caseId"]).Company.id:
                return True
            else:
                return False
        return False


class hasawarenesspermission:
    def has_permission(self, request, view):
        userRole=parser(request)
        if userRole is None:
            return False
        if request.user == "AnonymousUser":
            return False
        if request.user and request.user.is_authenticated:
            if request.method == "POST":
                if userRole.has_perm('add_awarenessprogram') :
                    return True
            if request.method == "GET":
                if userRole.has_perm('view_awarenessprogram') :
                    return True
            if request.method == "PATCH":
                if userRole.has_perm('change_awarenessprogram') :
                    return True
            if request.method == "DELETE":
                if userRole.has_perm('delete_awarenessprogram') :
                    return True
        else:
            return False   

class hasincentivespermission:
    def has_permission(self, request, view):
        userRole=parser(request)
        if userRole is None:
            return False
        if request.user == "AnonymousUser":
            return False
        if request.user and request.user.is_authenticated:
            if request.method == "POST":
                if userRole.has_perm('view_incentives') :
                    return True
        else:
            return False   


def is_in_group(user, group_name,method,model):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """

    if method == "GET":
        # try:
        error = []
        permission = "view_" + model
        # print(Group.objects.get(name=group_name, permissions__codename='view_case').user_set.filter(id=user.id).exists())
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            error.append("Group Does not exist")
            return error, None
        if group in user.group_permissions.all():
            pass
        else:
            error.append("User Does not exist in group")
            return error, None

        try:
            
            Group.objects.get(name=group_name, permissions__codename=permission).role_set.filter(id=user.id).exists()
            
        except Group.DoesNotExist:
            error.append("The group does not have the required permissions")
            return error, None
        
        return None, Group.objects.get(name=group_name, permissions__codename=permission).role_set.filter(
            id=user.id).exists()
    if method == "PUT":
        error = []
        permission = "change_" + model
        # print(Group.objects.get(name=group_name, permissions__codename='view_case').user_set.filter(id=user.id).exists())
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            error.append("Group Does not exist")
            return error, None

        if group in user.group_permissions.all():
            pass
        else:
            error.append("User Does not exist in group")
            return error, None

        try:
            
            Group.objects.get(name=group_name, permissions__codename=permission).role_set.filter(id=user.id).exists()
            
        except Group.DoesNotExist:
            error.append("The group does not have the required permissions")
            return error, None
        
        return None, Group.objects.get(name=group_name, permissions__codename=permission).role_set.filter(
            id=user.id).exists()
    if method == "PATCH":
        error = []
        permission = "change_" + model
        # print(Group.objects.get(name=group_name, permissions__codename='view_case').user_set.filter(id=user.id).exists())
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            error.append("Group Does not exist")
            return error, None
        if group in user.group_permissions.all():
            pass
        else:
            error.append("User Does not exist in group")
            return error, None

        try:
            
            Group.objects.get(name=group_name, permissions__codename=permission).role_set.filter(id=user.id).exists()
            
        except Group.DoesNotExist:
            error.append("The group does not have the required permissions")
            return error, None
        
        return None, Group.objects.get(name=group_name, permissions__codename=permission).role_set.filter(
            id=user.id).exists()
    if method == "POST":
        error = []
        permission = "add_" + model
        # print(Group.objects.get(name=group_name, permissions__codename='view_case').user_set.filter(id=user.id).exists())
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            error.append("Group Does not exist")
            return error, None
        if group in user.group_permissions.all():
            pass
        else:
            error.append("User Does not exist in group")
            return error, None

        try:
            
            Group.objects.get(name=group_name, permissions__codename=permission).role_set.filter(id=user.id).exists()
            
        except Group.DoesNotExist:
            error.append("The group does not have the required permissions")
            return error, None
        
        return None, Group.objects.get(name=group_name, permissions__codename=permission).role_set.filter(
            id=user.id).exists()
    if method == "DELETE":
        error = []
        permission = "delete_" + model
        # print(Group.objects.get(name=group_name, permissions__codename='view_case').user_set.filter(id=user.id).exists())
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            error.append("Group Does not exist")
            return error, None

        if group in user.group_permissions.all():
            pass
        else:
            error.append("User Does not exist in group")
            return error, None

        try:
            
            Group.objects.get(name=group_name, permissions__codename=permission).role_set.filter(id=user.id).exists()
            
        except Group.DoesNotExist:
            error.append("The group does not have the required permissions")
            return error, None
        
        return None, Group.objects.get(name=group_name, permissions__codename=permission).role_set.filter(
            id=user.id).exists()


class HasGroupPermission(permissions.BasePermission):
    """
    Ensure user is in required groups.
    """
    # def __init__(self,model,required_groups_mapping):
    #     self.model = model
    #     self.required_groups_mapping = required_groups_mapping
    def has_permission(self, request, view):
        # Get a mapping of methods -> required group.
        
        required_groups_mapping = getattr(view, "required_groups", {})
        model = getattr(view, "model", "")
        # Determine the required groups for this particular request method.
        required_groups = required_groups_mapping.get(request.method, [])
        # Return True if the user has all the required groups or is staff.
        # print(is_in_group(request.user, group_name,request.method) )
        group_checks = []
        exception_send = []
        userRole=parser(request)
        if userRole is None:
                raise exceptions.PermissionDenied({"error":"ROLE ID NOT PRESENT"})
        # Loop over each group name in the list of required groups
        for group_name in required_groups:
            # If the group name is not "__all__", check if the user is in the group
            if group_name != "__all__":
                # print(group_name)
                # if check
                error, \
                    check = is_in_group(userRole.role, group_name, request.method, model)
                # print(check)
            # If the group name is "__all__", set check to True
            else:
                check = True

            # Append the result of the check to the list of group checks

            group_checks.append(check)
            exception_send.append(error)
        # Check if all the group checks are True
        is_user_in_required_groups = any(group_checks)

        if (is_user_in_required_groups == False):
            dic = {}
            for i in range(len(required_groups)):
                dic[required_groups[i]] = exception_send[i]
            raise exceptions.PermissionDenied(dic)
        # Check if the user is logged in and is a staff member
        is_user_staff = request.user and request.user.is_staff

        # Check if the user is in the required groups or is a staff member
        if is_user_in_required_groups or is_user_staff:
            # Do something
            return True
        else:
            return False

        # return any([is_in_group(request.user, group_name,request.method) if group_name != "__all__" else True for group_name in required_groups]) or (request.user and request.user.is_staff)