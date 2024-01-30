import datetime
from accounts.dateUtils import working_days, count_working_hours
from accounts.constants import ActionTypes, CaseActiveStatus, CaseStatus, UserRole
from accounts.models import AuditLog, BaseUserModel, Case, UserRoleFactory,Incentives
from accounts.serializers import CaseSerializers
import pytz
import math
from datetime import  timedelta
from rest_framework import  status
from django.utils.timezone import localtime
from accounts.utils import current_time
from accounts.Utils.userRoleParser import parser
from rest_framework.request import Request

def assign_cm(request:Request,userid,pk:int):
    userRole=parser(request)
    if userRole is None:
        return None,status.HTTP_400_BAD_REQUEST
    case_details = Case.objects.get(pk=pk)
    try:
        # cm=BaseUserModel.objects.get(pk=user_id,role=UserRole.CASE_MANAGER,company_fk=case_details.Company,factory_fk=case_details.Factory)
        # cm=UserRoleFactory.objects.get(user_fk=BaseUserModel.objects.get(pk=user_id),role=UserRole.CASE_MANAGER,user_fk__company_fk=case_details.Company,factory_fk=case_details.Factory)
        Date = localtime(case_details.T1vrfDate)
        # print(request.data, "dsdsdsds")
        data = request.data
        data["CaseStatus"] = CaseStatus.ASSIGNED_TO_MANAGER
        data["CurrentStatus"] = CaseActiveStatus.NEW_CASE
        startDate = Date
        endDate = current_time()
        data["T1vrfDate"] = endDate
        caseFreeze = Incentives.objects.get(Case=case_details)
        if caseFreeze.CRreceiveDate:
            #if caseFreeze.CRsendDate.date == caseFreeze.CRreceiveDate.date:
            #if case_details.CaseStatus == CaseStatus.ASSIGNED_TO_REPORTER:
                working_hours = count_working_hours(startDate,caseFreeze.CRsendDate,case_details.Factory) + count_working_hours(caseFreeze.CRreceiveDate,endDate,case_details.Factory)
                if working_hours < 24:
                    data["T0"] = 1
                    data["T0Breached"] = False
                else:
                    data["T0"] = math.ceil(working_hours/24)
                    data["T0Breached"] = True
        # elif (caseFreeze.CRsendDate is not None) and (caseFreeze.CRreceiveDate is None):
        #     caseFreeze.valid = False
        #     data["T0Breached"] = False
        else:
            days = working_days(startDate, endDate, case_details.Factory)
            if days <= 1:
                data["T0"] = 1
                data["T0Breached"] = False
            else:
                data["T0"] = days
                data["T0Breached"] = True
        serializer = CaseSerializers(
            case_details, data=request.data)
        if serializer.is_valid():
            newstate = serializer.save()
            auditlog = AuditLog.objects.create(
                case=case_details,
                status=case_details.CaseStatus,
                created_by=userRole,
                var_changed="CaseManager",
                prev_state="",
                current_state=request.data["CaseManager"],
                action_type=ActionTypes.CM_ASSIGNED,
            )
            return serializer.data, status.HTTP_200_OK
        else:
            return serializer.errors, status.HTTP_400_BAD_REQUEST
    except BaseUserModel.DoesNotExist:
        return "User Does not exist", status.HTTP_400_BAD_REQUEST
