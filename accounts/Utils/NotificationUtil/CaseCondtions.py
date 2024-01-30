from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.contrib.auth.models import Permission
from accounts.constants import ActionTypes, CaseActiveStatus, CaseStatus, UserRole
from accounts.models import Case, BaseUserModel, Factory, HolidayCalendar,UserRoleFactory, AuditLog  # Import your models
from django.conf import settings

class ConditionMappings:
    # time <= caseDate + 18 hours 
    # time -18 hours <= caseDate 
    # caseDate >= time - 18hours 
    start_of_today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    CONDITIONS = {
        'lastLoginCheck_role_gte_6': (UserRoleFactory, Q(last_login_role__gte= timezone.now() - timedelta(hours=6))),
        'user_is_active': (BaseUserModel, Q(is_active=True)),
        'user_created_recently' : (BaseUserModel, Q(created_at__gte=timezone.now() - timedelta(minutes=20))),
        'user_not_created_recently' : (BaseUserModel, Q(created_at__lte=timezone.now() - timedelta(minutes=20))),
        'role_is_active' : (UserRoleFactory, Q(is_active=True)),
        'role_is_cr': (UserRoleFactory, Q(role__role=UserRole.CASE_REPORTER, is_active=True)),
        'role_is_cm': (UserRoleFactory, Q(role__role=UserRole.CASE_MANAGER, is_active=True)),
        'role_is_ct': (UserRoleFactory, Q(role__role=UserRole.CASE_TROUBLESHOOTER, is_active=True)),
        'role_is_sa': (UserRoleFactory, Q(role__role=UserRole.SUPER_ADMIN, is_active=True)),
        'role_is_ra': (UserRoleFactory, Q(role__role=UserRole.REGIONAL_ADMIN, is_active=True)),
        'role_is_fa': (UserRoleFactory, Q(role__role=UserRole.FACTORY_ADMIN, is_active=True)),
        'role_is_ra_or_fa': (UserRoleFactory, Q(role__role=UserRole.REGIONAL_ADMIN, is_active=True) | Q(role__role=UserRole.FACTORY_ADMIN, is_active=True)),
        'role_is_ra_or_sa': (UserRoleFactory, Q(role__role=UserRole.REGIONAL_ADMIN, is_active=True) | Q(role__role=UserRole.SUPER_ADMIN, is_active=True)),
        'role_created_recently': (UserRoleFactory, Q(created_at__gte=timezone.now() - timedelta(minutes=20), is_active=True)),
        'case_details_empty' : (Case, Q(CaseDetails=None)),
        'case_report_empty_cr' : (Case, Q(CaseStatus=CaseStatus.ASSIGNED_TO_REPORTER )),
        'auditLog_caseUploaded_cr' : (AuditLog, Q(action_type=ActionTypes.CASE_CREATE, status= CaseStatus.ASSIGNED_TO_REPORTER )),
        'auditLog_caseTransferred_cm' : (AuditLog, Q(action_type=ActionTypes.CM_ASSIGNED, status =CaseStatus.ASSIGNED_TO_MANAGER)),
        'auditLog_caseTransferred_ct' : (AuditLog, Q(action_type=ActionTypes.CT_ASSIGNED, status =CaseStatus.ASSIGNED_TO_TROUBLESHOOTER)),
        'auditLog_caseTransferred_ra' : (AuditLog, Q(action_type=ActionTypes.RA_ASSIGNED, status = CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN)),
        'auditLog_caseTransferred_ra_recently' : (AuditLog, Q(action_type=ActionTypes.RA_ASSIGNED, status = CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN, created_at__gte= timezone.now() - timedelta(minutes=20))),
        'auditLog_caseTransferred_ra_and_morethan_24hours_passed' : (AuditLog, Q(action_type=ActionTypes.RA_ASSIGNED, status = CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN, created_at__lte= timezone.now() - timedelta(hours=24))),
        
        'auditLog_case_unresponsive' : (AuditLog, Q(status = CaseStatus.UNRESPONSIVE, action_type= ActionTypes.CASE_UNRESPONSIVE)),
        'case_unresponsive_with_ct' : (Case, Q(CaseStatus= CaseStatus.UNRESPONSIVE, Troubleshooter = not None, RegionalAdmin = None)),
        'case_unresponsive_with_ra' : (Case, Q(CaseStatus= CaseStatus.UNRESPONSIVE, Troubleshooter = None, RegionalAdmin = not None)),

        'POSH_case' :  (Case, Q(CaseStatus = CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN) | Q(CaseStatus = CaseStatus.RA_INVESTIGATION)),
        # 'AuditLog_Transferred_Found_but_not_SMS' : (AuditLog, Q(action_type = ))
        

        'startDate_today_auditLog' : (AuditLog, Q(created_at__gt=start_of_today)),
        'startDate_2dayAgo_auditLog': (AuditLog, Q(created_at__gt=(timezone.now() - timedelta(days=2)))),

        'case_in_draft_cr': (Case, Q(CurrentStatus=CaseActiveStatus.DRAFT, CaseStatus= CaseStatus.ASSIGNED_TO_REPORTER)),
        'case_in_draft_cm': (Case, Q(CurrentStatus=CaseActiveStatus.DRAFT, CaseStatus= CaseStatus.ASSIGNED_TO_MANAGER)),
        'case_in_draft_ct': (Case, Q(CurrentStatus=CaseActiveStatus.DRAFT, CaseStatus= CaseStatus.ASSIGNED_TO_TROUBLESHOOTER)),
        'case_in_draft_ra': (Case, Q(CurrentStatus=CaseActiveStatus.DRAFT, CaseStatus= CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN)),
        'case_in_draft_or_unread_or_new_ra': (Case, Q(CurrentStatus=CaseActiveStatus.DRAFT, CaseStatus= CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN) | Q(CurrentStatus=CaseActiveStatus.UNREAD, CaseStatus = CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN ) | Q(CurrentStatus=CaseActiveStatus.NEW_CASE, CaseStatus = CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN )),
        'auditLog_worker_message_cr' : (AuditLog, Q(action_type = ActionTypes.REVERT_MESSAGE) & Q(status = CaseStatus.ASSIGNED_TO_REPORTER)),
        'auditLog_worker_message_cm' : (AuditLog, Q(action_type = ActionTypes.REVERT_MESSAGE) & Q(status = CaseStatus.ASSIGNED_TO_MANAGER)),
        'auditLog_worker_message_ct' : (AuditLog, Q(action_type = ActionTypes.REVERT_MESSAGE) & Q(status__in = [CaseStatus.ASSIGNED_TO_TROUBLESHOOTER , CaseStatus.UNDER_INVESTIGATION, CaseStatus.RE_INVESTIGATION , CaseStatus.RESOLVED,CaseStatus.CLOSED ])),
        'auditLog_worker_message_ra' : (AuditLog, Q(action_type = ActionTypes.REVERT_MESSAGE) & Q(status__in = [CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN, CaseStatus.RA_INVESTIGATION, CaseStatus.RE_INVESTIGATION_RA, CaseStatus.RESOLVED, CaseStatus.CLOSED ])),
        'userRole_Updated_At_Changed_or_Created_at': ( UserRoleFactory, Q(updated_at__gte=timezone.now() - timedelta(minutes=20)) | Q(created_at__gte=timezone.now() - timedelta(minutes=20))),
        'last_20mins_Updated_at_Change' : (UserRoleFactory, Q(updated_at__gte=timezone.now() - timedelta(minutes=20))),
        'role_is_not_active' : (UserRoleFactory, Q(is_active=False)),
        'auditLog_caseTransferred_SPLIT_MERGE_ASSIGN' : ( AuditLog, Q(action_type = ActionTypes.CASE_TRANSFERED_ASSIGN,  created_at__gte = timezone.now() - timedelta(minutes=10)) | Q(action_type = ActionTypes.CASE_TRANSFERED_MERGE,  created_at__gte = timezone.now() - timedelta(minutes=10)) | Q(action_type = ActionTypes.CASE_TRANSFERED_SPLIT,  created_at__gte = timezone.now() - timedelta(minutes=10))),
        # 'userRole_Created_At_Changed' : (UserRoleFactory, Q(created_at__gte=timezone.now() - timedelta(minutes=20))),
        'permission_awareness_program' : (Permission, Q(codename="add_awareness_program")),
        'holiday_in_next_2Days': (HolidayCalendar, Q(startDate__gte=timezone.now(), startDate__lte=timezone.now() + timedelta(hours=48))),
        'factory_is_active' : (Factory, Q(is_active=True)),
        'case_with_cr': (Case, Q(CaseStatus=CaseStatus.ASSIGNED_TO_REPORTER)),
        'case_with_cm': (Case, Q(CaseStatus=CaseStatus.ASSIGNED_TO_MANAGER)),
        'case_with_ct': (Case, Q(CaseStatus=CaseStatus.ASSIGNED_TO_TROUBLESHOOTER)),
        'case_with_high_priority': (Case, Q(Priority= "Major Grievance (Level 1)") | Q(Priority="Major Grievance (Level 2)")),
        'case_with_medium_priority': (Case, Q(Priority= "Medium Grievance (Internal)") | Q(Priority="Medium Grievance (External)")),
        'case_with_low_priority': (Case, Q(Priority= "Minor Grievance (Internal)") | Q(Priority="Minor Grievance (External)")),
        'case_with_priority_medium_external':(Case, Q(Priority="Medium Grievance (External)")),
        'case_with_priority_medium_internal':(Case, Q(Priority= "Medium Grievance (Internal)")),
        'case_with_priority_minor_external':(Case,  Q(Priority="Minor Grievance (External)")),
        'case_with_priority_minor_internal':(Case,  Q(Priority= "Minor Grievance (Internal)")),
        # 'userRole_awareness_program_perm' : (Permission, Q(codename='add_awareness_program')),
    }