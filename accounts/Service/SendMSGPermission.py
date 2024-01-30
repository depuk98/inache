from accounts.constants import CaseStatus, UserRole
from accounts.Utils.userRoleParser import parser
from rest_framework.request import Request
from accounts.models import Case
def send_message_user_validation(case:Case,request:Request):
    userRole=parser(request)
    if userRole is None:
        return False
    if userRole.role.role == UserRole.CASE_REPORTER:
        if case.CaseStatus == CaseStatus.ASSIGNED_TO_REPORTER:
            return True
        else:
            return False

    elif userRole.role.role == UserRole.CASE_MANAGER:
        if case.CaseStatus == CaseStatus.ASSIGNED_TO_MANAGER:
            return True
        else:
            return False

    elif userRole.role.role == UserRole.CASE_TROUBLESHOOTER:
        if case.CaseStatus == CaseStatus.ASSIGNED_TO_TROUBLESHOOTER or case.CaseStatus == CaseStatus.UNDER_INVESTIGATION or case.CaseStatus == CaseStatus.RESOLVED or case.CaseStatus == CaseStatus.RE_INVESTIGATION:
            return True
        else:
            return False