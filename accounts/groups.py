from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.constants import UserRole
from accounts.models import Role, UserRoleFactory, Company, IncentivePermission
# from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission



def S_ADMIN(data:dict,userRole:UserRoleFactory)->None:
    new_group, created = Group.objects.get_or_create(name='SUPER_ADMIN')
    # new_group.permissions.clear()
    add_bum = Permission.objects.get(codename='add_baseusermodel')
    change_bum = Permission.objects.get(codename='change_baseusermodel')
    view_bum = Permission.objects.get(codename='view_baseusermodel')
    delete_bum = Permission.objects.get(codename='delete_baseusermodel')
    add_factory = Permission.objects.get(codename='add_factory')
    change_factory = Permission.objects.get(codename='change_factory')
    view_factory = Permission.objects.get(codename='view_factory')
    delete_factory = Permission.objects.get(codename='delete_factory')
    crud_facadmin = Permission.objects.get(codename='crud_factory_admin')
    crud_cr = Permission.objects.get(codename='crud_cr')
    crud_cm = Permission.objects.get(codename='crud_cm')
    crud_ct = Permission.objects.get(codename='crud_ct')
    view_case=Permission.objects.get(codename='view_case')
    view_reg = Permission.objects.get(codename='view_factoryregion')
    add_reg = Permission.objects.get(codename='add_factoryregion')
    change_reg = Permission.objects.get(codename='change_factoryregion')
    delete_reg = Permission.objects.get(codename='delete_factoryregion')
    add_holidaycal = Permission.objects.get(codename='add_holidaycalendar')
    view_holidaycal = Permission.objects.get(codename='view_holidaycalendar')
    change_holidaycal = Permission.objects.get(codename='change_holidaycalendar')
    delete_holidaycal = Permission.objects.get(codename='delete_holidaycalendar')
    add_awarenessprogram = Permission.objects.get(codename='add_awarenessprogram')
    view_awarenessprogram = Permission.objects.get(codename='view_awarenessprogram')
    change_awarenessprogram = Permission.objects.get(codename='change_awarenessprogram')
    delete_awarenessprogram = Permission.objects.get(codename='delete_awarenessprogram')
    add_broadcastmessage = Permission.objects.get(codename='add_broadcastmessage')
    view_broadcastmessage = Permission.objects.get(codename='view_broadcastmessage')
    change_broadcastmessage = Permission.objects.get(codename='change_broadcastmessage')
    delete_broadcastmessage = Permission.objects.get(codename='delete_broadcastmessage')
    
    
            # userRole.user_permissions.add(add_holidaycal,view_holidaycal,change_holidaycal,delete_holidaycal)

    view_casereslovingreport=Permission.objects.get(codename='view_casereslovingreport')
    assign_permissions(data,userRole)

    creator_permissions = [
        add_bum,
        change_bum,
        view_bum,
        delete_bum,
        add_factory,
        change_factory,
        view_factory,
        delete_factory,
        crud_facadmin,
        crud_cr,
        crud_cm,
        crud_ct,
        view_case,
        view_casereslovingreport,
        view_reg,
        add_reg,
        change_reg,
        delete_reg,
        view_casereslovingreport,
        add_holidaycal,
        view_holidaycal,
        change_holidaycal,
        delete_holidaycal,
        # add_awarenessprogram,
        view_awarenessprogram,
        # change_awarenessprogram,
        # delete_awarenessprogram,
        add_broadcastmessage,
        view_broadcastmessage,
        change_broadcastmessage,
        delete_broadcastmessage
    ]
    
    assign_permissions(data,userRole)

    role=Role.objects.get(role='SUPER_ADMIN')
    new_group.permissions.set(creator_permissions)
    role.group_permissions.add(new_group)
    
def R_ADMIN(data,userRole):
    new_group, created = Group.objects.get_or_create(name='REGIONAL_ADMIN')
    # new_group.permissions.clear()
    view_bum = Permission.objects.get(codename='view_baseusermodel')
    add_bum = Permission.objects.get(codename='add_baseusermodel')
    change_bum = Permission.objects.get(codename='change_baseusermodel')
    delete_bum = Permission.objects.get(codename='delete_baseusermodel')
    view_factory = Permission.objects.get(codename='view_factory')
    add_factory = Permission.objects.get(codename='add_factory')
    change_factory = Permission.objects.get(codename='change_factory')
    delete_factory = Permission.objects.get(codename='delete_factory')
    crud_facadmin = Permission.objects.get(codename='crud_factory_admin')
    crud_cr = Permission.objects.get(codename='crud_cr')
    crud_cm = Permission.objects.get(codename='crud_cm')
    crud_ct = Permission.objects.get(codename='crud_ct')
    view_case=Permission.objects.get(codename='view_case')
    add_case = Permission.objects.get(codename='add_case')
    change_case = Permission.objects.get(codename='change_case')
    view_casereslovingreport=Permission.objects.get(codename='view_casereslovingreport')
    add_casereslovingreport = Permission.objects.get(codename='add_casereslovingreport')
    change_casereslovingreport = Permission.objects.get(codename='change_casereslovingreport')
    view_reg = Permission.objects.get(codename='view_factoryregion')
    add_holidaycal = Permission.objects.get(codename='add_holidaycalendar')
    view_holidaycal = Permission.objects.get(codename='view_holidaycalendar')
    change_holidaycal = Permission.objects.get(codename='change_holidaycalendar')
    delete_holidaycal = Permission.objects.get(codename='delete_holidaycalendar')
    add_awarenessprogram = Permission.objects.get(codename='add_awarenessprogram')
    view_awarenessprogram = Permission.objects.get(codename='view_awarenessprogram')
    change_awarenessprogram = Permission.objects.get(codename='change_awarenessprogram')
    delete_awarenessprogram = Permission.objects.get(codename='delete_awarenessprogram')
    add_broadcastmessage = Permission.objects.get(codename='add_broadcastmessage')
    view_broadcastmessage = Permission.objects.get(codename='view_broadcastmessage')
    change_broadcastmessage = Permission.objects.get(codename='change_broadcastmessage')
    delete_broadcastmessage = Permission.objects.get(codename='delete_broadcastmessage')
    assign_permissions(data,userRole)

    creator_permissions = [
        view_bum,
        add_bum,
        change_bum,
        delete_bum,
        add_factory,
        change_factory,
        view_factory,
        delete_factory,
        crud_facadmin,
        crud_cr,
        crud_cm,
        crud_ct,
        view_case,
        add_case,
        change_case,
        view_casereslovingreport,
        add_casereslovingreport,
        change_casereslovingreport,
        view_reg,
        add_holidaycal,
        view_holidaycal,
        change_holidaycal,
        delete_holidaycal,
        # add_awarenessprogram,
        view_awarenessprogram,
        # change_awarenessprogram,
        # delete_awarenessprogram,
        add_broadcastmessage,
        view_broadcastmessage,
        change_broadcastmessage,
        delete_broadcastmessage
    ]
    assign_permissions(data,userRole)

    role=Role.objects.get(role='REGIONAL_ADMIN')
    new_group.permissions.set(creator_permissions)
    role.group_permissions.add(new_group)


def F_ADMIN(data:dict,userRole:UserRoleFactory)->None:
    new_group, created = Group.objects.get_or_create(name='FACTORY_ADMIN')
    
    add_bum = Permission.objects.get(codename='add_baseusermodel')
    change_bum = Permission.objects.get(codename='change_baseusermodel')
    view_bum = Permission.objects.get(codename='view_baseusermodel')
    delete_bum = Permission.objects.get(codename='delete_baseusermodel')
    change_factory = Permission.objects.get(codename='change_factory')
    view_factory = Permission.objects.get(codename='view_factory')
    crud_facadmin = Permission.objects.get(codename='crud_factory_admin')
    crud_cr = Permission.objects.get(codename='crud_cr')
    crud_cm = Permission.objects.get(codename='crud_cm')
    crud_ct = Permission.objects.get(codename='crud_ct')
    view_case=Permission.objects.get(codename='view_case')
    view_reg = Permission.objects.get(codename='view_factoryregion')
    view_casereslovingreport=Permission.objects.get(codename='view_casereslovingreport')
    view_holidaycal = Permission.objects.get(codename='view_holidaycalendar')

    assign_permissions(data,userRole)

    creator_permissions = [
        view_holidaycal,
        add_bum,
        change_bum,
        view_bum,
        delete_bum,
        change_factory,
        view_factory,
        crud_facadmin,
        crud_cr,
        crud_cm,
        crud_ct,
        view_case,
        view_casereslovingreport,
        view_reg
    ]
    assign_permissions(data,userRole)
    role=Role.objects.get(role='FACTORY_ADMIN')
    new_group.permissions.set(creator_permissions)
    role.group_permissions.add(new_group)


def CR_group(data:dict,userRole:UserRoleFactory)->None:
    new_group, created = Group.objects.get_or_create(name='CR')
    view_bum = Permission.objects.get(codename='view_baseusermodel')
    change_bum = Permission.objects.get(codename='change_baseusermodel')
    view_factory = Permission.objects.get(codename='view_factory')
    crud_facadmin = Permission.objects.get(codename='crud_factory_admin')
    crud_cr = Permission.objects.get(codename='crud_cr')
    crud_cm = Permission.objects.get(codename='crud_cm')
    crud_ct = Permission.objects.get(codename='crud_ct')
    add_case = Permission.objects.get(codename='add_case')
    view_case=Permission.objects.get(codename='view_case')
    change_case = Permission.objects.get(codename='change_case')
    # view_holidaycal = Permission.objects.get(codename='view_holidaycalendar')
    view_reg = Permission.objects.get(codename='view_factoryregion')
    creator_permissions = [
        view_bum,
        change_bum,
        view_factory,
        crud_facadmin,
        crud_cr,
        crud_cm,
        crud_ct,
        add_case,
        view_case,
        change_case,
        view_reg,
        # view_holidaycal
    ]
    assign_permissions(data,userRole)
    role=Role.objects.get(role='CR')
    new_group.permissions.set(creator_permissions)
    role.group_permissions.add(new_group)
    


def CM_group(data:dict,userRole:UserRoleFactory)->None:
    new_group, created = Group.objects.get_or_create(name='CM')
    view_bum = Permission.objects.get(codename='view_baseusermodel')
    change_bum = Permission.objects.get(codename='change_baseusermodel')
    view_factory = Permission.objects.get(codename='view_factory')
    crud_facadmin = Permission.objects.get(codename='crud_factory_admin')
    crud_cr = Permission.objects.get(codename='crud_cr')
    crud_cm = Permission.objects.get(codename='crud_cm')
    crud_ct = Permission.objects.get(codename='crud_ct')
    add_case = Permission.objects.get(codename='add_case')
    view_case=Permission.objects.get(codename='view_case')
    change_case = Permission.objects.get(codename='change_case')
    view_reg = Permission.objects.get(codename='view_factoryregion')
    view_holidaycal = Permission.objects.get(codename='view_holidaycalendar')

    creator_permissions = [
        view_bum,
        change_bum,
        view_factory,
        crud_facadmin,
        crud_cr,
        crud_cm,
        crud_ct,
        add_case,
        view_case,
        change_case,
        view_reg,
        view_holidaycal
    ]
    assign_permissions(data,userRole)
    role=Role.objects.get(role='CM')
    new_group.permissions.set(creator_permissions)
    role.group_permissions.add(new_group)


def CT_group(data:dict,userRole:UserRoleFactory)->None:
    new_group, created = Group.objects.get_or_create(name='CT')
    view_bum = Permission.objects.get(codename='view_baseusermodel')
    change_bum = Permission.objects.get(codename='change_baseusermodel')
    view_factory = Permission.objects.get(codename='view_factory')
    crud_facadmin = Permission.objects.get(codename='crud_factory_admin')
    crud_cr = Permission.objects.get(codename='crud_cr')
    crud_cm = Permission.objects.get(codename='crud_cm')
    crud_ct = Permission.objects.get(codename='crud_ct')
    add_case = Permission.objects.get(codename='add_case')
    view_case=Permission.objects.get(codename='view_case')
    change_case = Permission.objects.get(codename='change_case')
    add_casereslovingreport = Permission.objects.get(codename='add_casereslovingreport')
    view_casereslovingreport=Permission.objects.get(codename='view_casereslovingreport')
    change_casereslovingreport = Permission.objects.get(codename='change_casereslovingreport')
    view_holidaycal = Permission.objects.get(codename='view_holidaycalendar')
    view_reg = Permission.objects.get(codename='view_factoryregion')
    creator_permissions = [
        view_bum,
        change_bum,
        view_factory,
        crud_facadmin,
        crud_cr,
        crud_cm,
        crud_ct,
        add_case,
        view_case,
        change_case,
        add_casereslovingreport,
        view_casereslovingreport,
        change_casereslovingreport,
        view_reg,
        view_holidaycal
        
    ]
    assign_permissions(data,userRole)
    role=Role.objects.get(role='CT')
    new_group.permissions.set(creator_permissions)
    role.group_permissions.add(new_group)

def assign_permissions(data:dict,userRole:UserRoleFactory)->None:
    if data["user_permissions"]["hasAccess_BroadCast_Message"] == "true":
        addbroadcastperm = Permission.objects.get(
            codename='add_broadcastmessage')
        viewbroadcastperm = Permission.objects.get(
            codename='view_broadcastmessage')
        changebroadcastperm = Permission.objects.get(
            codename='change_broadcastmessage')
        userRole.user_permissions.add(addbroadcastperm,viewbroadcastperm,changebroadcastperm)
    if data["user_permissions"]["hasAccess_Holiday_Calender"] == "true":
        if data['role']==UserRole.FACTORY_ADMIN or data['role']==UserRole.DEFAULT_ROLE or data['role']==UserRole.REGIONAL_ADMIN:
            add_holidaycal = Permission.objects.get(codename='add_holidaycalendar')
            view_holidaycal = Permission.objects.get(codename='view_holidaycalendar')
            change_holidaycal = Permission.objects.get(codename='change_holidaycalendar')
            delete_holidaycal = Permission.objects.get(codename='delete_holidaycalendar')
            userRole.user_permissions.add(add_holidaycal,view_holidaycal,change_holidaycal,delete_holidaycal)
        elif data["role"]==UserRole.CASE_REPORTER or data["role"]==UserRole.CASE_MANAGER  or data["role"]==UserRole.CASE_TROUBLESHOOTER :
            add_holidaycal = Permission.objects.get(codename='add_holidaycalendar')
            change_holidaycal = Permission.objects.get(codename='change_holidaycalendar')
            delete_holidaycal = Permission.objects.get(codename='delete_holidaycalendar')
            userRole.user_permissions.add(add_holidaycal,change_holidaycal,delete_holidaycal)
    
        
    if data["user_permissions"]["hasAccess_Awareness_Program"] == "true":
        print("hassaccess perms if")
        if data['role']==UserRole.CASE_REPORTER or data['role']==UserRole.CASE_TROUBLESHOOTER:
            add_awarepgm = Permission.objects.get(codename='add_awarenessprogram')
            view_awarepgm = Permission.objects.get(codename='view_awarenessprogram')
            # change_awarepgm = Permission.objects.get(codename='change_awareness_program')
            userRole.user_permissions.add(add_awarepgm,view_awarepgm)

    if Company.objects.get(Legalcompanyname="Shahi Exports PVT LTD").id != int(data["company_fk"]):
        view_incntvs = Permission.objects.get(codename='view_incentives', content_type__app_label='accounts', content_type__model='incentivepermission')
        userRole.user_permissions.add(view_incntvs)
         

def get_group_permissions(groups):
    try:
        for group in groups.iterator():
            groupobj = Group.objects.get(id=group.id)
            permissions = groupobj.permissions.all()
            return permissions
    except Group.DoesNotExist:
        return None