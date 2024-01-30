import datetime
from accounts.constants import CaseActiveStatus, CaseStatus, ActionTypes, UserRole
from accounts.models import Case, AuditLog, BaseUserModel, UserRoleFactory
from accounts.serializers import CaseSerializers
import pytz
import random
from rest_framework import  status

from accounts.Utils.userRoleParser import parser

def assign_ra(request,pk):
    userRole=parser(request)
    if userRole is None:
        return None,status.HTTP_400_BAD_REQUEST
    case_details = Case.objects.get(pk=pk)
    try:
        data = request.data
        data["CaseStatus"] = CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN
        data["CurrentStatus"] = CaseActiveStatus.NEW_CASE
        # data["RegionalAdmin"] = assignRA(case_details)

        serializer = CaseSerializers(
            case_details, data=request.data)

        if serializer.is_valid():
            newstate = serializer.save()
            auditlog = AuditLog.objects.create(
            case=case_details,
            status=case_details.CaseStatus,
            created_by=userRole,
            prev_state=str(case_details),
            current_state=str(case_details),
            action_type=ActionTypes.RA_ASSIGNED,
            )

            return serializer.data, status.HTTP_200_OK
        else:
            return serializer.errors, status.HTTP_400_BAD_REQUEST
    except BaseUserModel.DoesNotExist:
        return "User Does not exist", status.HTTP_400_BAD_REQUEST




def assignRA(case):

    data = {}
    ra = UserRoleFactory.objects.filter(user_fk__company_fk=case.Company,region_fk=case.Factory.region,role__role=UserRole.REGIONAL_ADMIN,is_active=True,user_fk__is_active=True)
    if ra.count() == 1:
        case.RegionalAdmin = ra[0]
        case.save()
        return ra[0].id
    elif (ra.count() == 0):
        return "not assigned"
    for item in ra:
        cs = Case.objects.filter(RegionalAdmin=item)
        data[item] = cs.count()

    temp = min(data.values())
    res = [key for key in data if data[key] == temp]
    if (len(res) > 1):
        ran = random.choice(res)
        case.RegionalAdmin = ran
        case.save()
        return ran.id
    elif (len(res) == 1):
        case.RegionalAdmin = res[0]
        case.save()
        return res[0].id




