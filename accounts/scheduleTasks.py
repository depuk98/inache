from datetime import date
import datetime
from accounts.constants import UserRole, scheduleType, ActionTypes, CaseStatus
from accounts.dateUtils import is_working_day
from accounts.models import UserRoleFactory, scheduleInformation, SMSTemplates, AuditLog, Case, BaseUserModel, Company
from accounts.views import sendcasemessage, unResponsiveMessage
from accounts.utils import current_time

def checkForTasks():
    # gets all the tasks that were active
    tasks = scheduleInformation.objects.filter(is_active=True)
    for task in tasks:
        if task.type == scheduleType.SEND_MESSAGE:
            case = Case.objects.filter(id=task.Information["Case"])
            if case.exists():
                case = Case.objects.get(id=task.Information["Case"])
                company = Company.objects.get(id=task.Information["Company"])
                # only execute if its a working day
                if is_working_day(date.today(), case.Factory):
                    if task.count <= 2:
                        message = sendcasemessage(
                            task.Information["templateID"],
                            task.Information["body"],
                            task.Information["PhoneNo"],
                            company
                        )
                        auditlog = AuditLog.objects.create(
                            case=case,
                            status=case.CaseStatus,
                            created_by=UserRoleFactory.objects.get(role__role=UserRole.DEFAULT_ROLE),
                            prev_state="",
                            current_state="",
                            message=task.Information["body"],
                            action_type=ActionTypes.FOLLOWUP_MESSAGE_SENT,
                        )
                    task.count = task.count + 1
                    task.save()
                    # if required number of reminders sent, make the task inactive
                    if task.count == 4:
                        task.is_active = False
                        task.save()
                        case.CaseStatus = CaseStatus.UNRESPONSIVE
                        case.ClosingTime = current_time()
                        case.save()
                        auditlog = AuditLog.objects.create(
                            case=case,
                            status=case.CaseStatus,
                            created_by=UserRoleFactory.objects.get(role__role=UserRole.DEFAULT_ROLE),
                            prev_state="",
                            current_state="",
                            action_type=ActionTypes.CASE_UNRESPONSIVE,
                        )
                        language = SMSTemplates.objects.get(Company=company,
                                                            templateID=task.Information["templateID"]).language
                        template = SMSTemplates.objects.get(Company=company,
                                                            template_categories__contains=['Unresponsive Message'],
                                                            language=language)
                        templateID = template.templateID
                        body = template.body
                        response = unResponsiveMessage(case,body)
                        message = sendcasemessage(
                            templateID,
                            response,
                            task.Information["PhoneNo"],
                            company
                        )
                        auditlog = AuditLog.objects.create(
                            case=case,
                            status=case.CaseStatus,
                            created_by=UserRoleFactory.objects.get(role__role=UserRole.DEFAULT_ROLE),
                            prev_state="",
                            current_state="",
                            message=response,
                            action_type=ActionTypes.UNRESPONSIVE_MESSAGE_SENT,
                        )

            else:
                task.delete()

