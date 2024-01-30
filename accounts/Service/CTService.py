import datetime
from accounts.Utils import userRoleParser
from accounts.dateUtils import working_days, count_working_hours
from accounts.constants import ActionTypes, CaseActiveStatus, CaseStatus, UserRole
from accounts.models import AuditLog, BaseUserModel, Case, Incentives,UserRoleFactory
from accounts.serializers import CaseSerializers
from rest_framework import  status
import pytz
import math
from django.utils.timezone import localtime
from rest_framework.request import Request
from accounts.utils import current_time


def assign_ct(request:Request,user_id,pk:int):
    userRole=userRoleParser.parser(request)
    if userRole is None:
        return  None,status.HTTP_400_BAD_REQUEST
    case_details = Case.objects.get(pk=pk)
    try:
        # ct=BaseUserModel.objects.get(pk=user_id,role=UserRole.CASE_TROUBLESHOOTER,company_fk=case_details.Company,factory_fk=case_details.Factory)
        # cm=UserRol¸eFactory.objects.get(user_fk=BaseUserModel.objects.get(pk=user_id),role=UserRole.CASE_TROUBLESHOOTER,user_fk__company_fk=case_details.Company,factory_fk=case_details.Factory)

        T1vrfDate = localtime(case_details.T1vrfDate)
        data = request.data
        data["CaseStatus"] = CaseStatus.ASSIGNED_TO_TROUBLESHOOTER
        data["CurrentStatus"] = CaseActiveStatus.NEW_CASE
        startDate = T1vrfDate
        endDate = current_time()
        data["T2vrfDate"] = endDate
        caseFreeze = Incentives.objects.get(Case=case_details)
        # if caseFreeze.valid == False:
        #     data["T1Breached"] = False
        # elif (caseFreeze.CMsendDate is not None) and (caseFreeze.CMreceiveDate is None):
        #     caseFreeze.valid = False
        #     data["T1Breached"] = False
        if caseFreeze.CMreceiveDate:
            working_hours = count_working_hours(startDate,caseFreeze.CMsendDate,case_details.Factory) + count_working_hours(caseFreeze.CMreceiveDate,endDate,case_details.Factory)
            if working_hours < 24:
                data["T1"] = 1
                data["T1Breached"] = False
            else:
                data["T1"] = math.ceil(working_hours/24)
                data["T1Breached"] = True
        else:
            days = working_days(startDate, endDate, case_details.Factory)
            if days <= 1:
                data["T1"] = 1
                data["T1Breached"] = False
            else:
                data["T1"] = days
                data["T1Breached"] = True
        data["T2Breached"] = None
        serializer = CaseSerializers(case_details, data=request.data)
        if serializer.is_valid():
            newstate = serializer.save()
            auditlog = AuditLog.objects.create(
                case=case_details,
                status=case_details.CaseStatus,
                created_by=userRole,
                var_changed="CaseTroubleShooter",
                prev_state="",
                current_state=request.data["CaseTroubleShooter"],
                action_type=ActionTypes.CT_ASSIGNED,
            )

            return serializer.data,status.HTTP_200_OK
        else:
            return serializer.errors, status.HTTP_400_BAD_REQUEST
    except BaseUserModel.DoesNotExist:
        return "User Does not exist", status.HTTP_400_BAD_REQUEST
