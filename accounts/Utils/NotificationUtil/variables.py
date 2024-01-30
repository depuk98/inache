from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from accounts.Service.CasesService import dueDate
from accounts.models import Case, BaseUserModel, Factory, HolidayCalendar, Role,UserRoleFactory, AuditLog  # Import your models

class VariablesMapping:
    VARIABLES = {
        "user_name": {"model": BaseUserModel, "field": "name", "id_field": "id","key":"user_id"},
        "user_email": {"model": BaseUserModel, "field": "email", "id_field": "id","key":"user_id"},
        "case_number": {"model": Case, "field": "CaseNumber", "id_field": "id","key":"case_id"},
        "case_assgined_to_CM_datetime": {"model": Case, "field": "T1vrfDate", "id_field": "id","key":"case_id"},
        "case_assgined_to_CT_datetime": {"model": Case, "field": "T2vrfDate", "id_field": "id","key":"case_id"},
        "factory_unit_number": {"model" : Factory, "field": "Code", "id_field": "id", "key":"factory_fk" },
        "case_CR": {"model": Case, "field": "CaseReporter", "id_field": "id","key":"case_id"},
        "case_CM": {"model": Case, "field": "CaseManager", "id_field": "id","key":"case_id"},
        "case_CT": {"model": Case, "field": "CaseTroubleShooter", "id_field": "id","key":"case_id"},
        "case_RA": {"model": Case, "field": "RegionalAdmin", "id_field": "id","key":"case_id"},
        # Add more mappings as needed
        'user_is_active': (BaseUserModel, Q(is_active=True)),
        'role_is_active' : (UserRoleFactory, Q(is_active=True)),
        # 'recent_audit': (AuditLog, Q(created_at__gt=timezone.now() - timedelta(days=1))),
        'case_details_empty' : (Case, Q(CaseDetails="")),
        'user_createdAt' : {"model": BaseUserModel, "field": "created_at", "id_field": "id","key":"user_id"},
        'role_createdAt' : {"model": UserRoleFactory, "field": "created_at", "id_field": "id","key":"role_id"},
        'auditlog_id' : {"model": AuditLog, "field": "id", "id_field": "id","key":"id"}


        #scheduled_awarenessPrograms
        #completed_awarenessPrograms
        #pending_awarenessPrograms
        #previous_role
        #new_role
        #a_brief_description_of_new_access_privileges
        #awarenessProgram_video
        #role
        #minimum_compliance_percentage
        #support_contact_no
        #link_to_xlsx_file_for_monthly_collated_cases
        #case_received_date
        #case_priority_level
        #weekly_collated_cases_xlxs_based_onPriority
    }
