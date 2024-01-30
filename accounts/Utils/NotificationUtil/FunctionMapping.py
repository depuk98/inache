import traceback
from django.utils import timezone
from datetime import timedelta
from accounts.Service.CasesService import dueDate
from accounts.constants import ActionTypes, CaseActiveStatus, CaseStatus
from django.contrib.auth.models import Permission
from accounts.dateUtils import holidayCheck, holidayCheckFactory
from accounts.models import Case, UserRoleFactory
import csv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from accounts.models import AuditLog, Case

def check_recent_login(user, hours=6):
    now = timezone.now()
    return user.last_login_role >= now - timedelta(hours=hours)

def check_holiday(Date, factory):
    holidayCheckFactory(Date, factory)
    return

def SLADueDateCalculation(queryset, **kwargs):
    # Assuming 'role' is passed in kwargs
    role = kwargs.get('role')
    cases = list(queryset.values())
    # Call dueDate function with each case and the role
    help = dueDate(cases, role)

    breached_cases = []

    for case in cases:
        if case.get('dueDateBreached') is True:
            breached_cases.append(case)
    print("breached_cases", breached_cases)
    return breached_cases

def reminder_poshcases(queryset):
    print()
    cases_toSend_reminder = []
    cases = list(queryset.values())
    print("here with cases", cases)
    for case in cases:
        if case['CaseCategory'] in ["POSH", "Special Cases"] and case['CaseStatus'] != CaseStatus.CLOSED:
            auditLogs = AuditLog.objects.filter(case=case['id'], action_type=ActionTypes.REVERT_MESSAGE)
            if not auditLogs.exists():
                print("couple exists")
                case_obj = Case.objects.get(id=case['id'])  # Fetch the case object if you need the complete model instance
                cases_toSend_reminder.append(case_obj)
    return cases_toSend_reminder

def check_action_after_worker_reply(queryset):
    cases_to_remind = []
    cases = list(queryset.values())
    print("here with cases", cases)
    for case in cases:
        if case['CaseCategory'] in ["POSH", "Special Cases"] and case['CaseStatus'] != CaseStatus.CLOSED:
            # Fetch the latest log entry for the case
            print("jereeere")
            latest_log = AuditLog.objects.filter(case=case["id"])
            print("resent logs ",latest_log)
            # Check if the latest log entry is a reply from the worker
            if latest_log and latest_log.action_type == ActionTypes.REVERT_MESSAGE:
                # Calculate the time since the worker's reply
                time_since_reply = timezone.now() - latest_log.timestamp
                # If it's been 6 hours or more since the worker's reply and it is the latest action
                if time_since_reply >= timedelta(hours=6):
                    case_obj = Case.objects.get(id=case['id'])  # Fetch the case object
                    cases_to_remind.append(case_obj)
    
    return cases_to_remind

def check_ra_case_closed(queryset):
    cases_closed = []
    cases = list(queryset.values())
    for case in cases:
        if case['CaseCategory'] in ["POSH", "Special Cases"] and case['CaseStatus'] in [CaseStatus.CLOSED, CaseStatus.UNRESPONSIVE] :
            case_obj = Case.objects.get(id=case['id'])  # Fetch the case object
            cases_closed.append(case_obj)


    return cases_closed
def POSH_Case_SMS_not_Sent(cases):
    cases_list_whos_posh_message_notsent = []
    for case in cases:
        if case.CaseStatus is not CaseStatus.CLOSED & case.CaseCategory is "POSH":
            auditLogs = AuditLog.objects.filter(case = case, action_type = ActionTypes.FOLLOWUP_MESSAGE_POSH_SENT_WRITTEN_COMPLAINT_RA )
            if not auditLogs.exists():
                case_obj = Case.object.get(id = case)
                cases_list_whos_posh_message_notsent.append(case_obj)
    return cases_list_whos_posh_message_notsent

def AwarenessProgram_Permission(queryset):
    result =[]
    for query in queryset:
        permission = Permission.objects.get(codename="add_awareness_program")
        if query.has_perm(permission):
            result.append(query)
    return result

def coallatecaserasafa(queryset, **kwargs):
    print("coallate")
    # print(queryset,kwargs)
    operation=kwargs.get('operation', None)
    users=queryset
    try:
        if operation=="weekly":
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            print(start_date,end_date)
        elif operation=="monthly":
            start_date = datetime.now() - relativedelta(months=1)
            end_date = datetime.now()
        user_xlsx={}
        
        for userRole in users:
            # userRole=UserRoleFactory.objects.get(id=user)
            cases = Case.objects.filter(Date__range=(start_date, end_date),Company=userRole.user_fk.company_fk)
            print("dadadadafdsjf dsjv dsjv ksdj ds vsdk")
            
            case_data=[]
            print("cases",len(cases),userRole)
            if len(cases)==0:
                continue
            for case in cases:  
                    
                case_data.append({
                    'Unit Number/ Factory Number': case.Factory.Code if case.Factory.Code is not None else '',
                    'Case Number': case.CaseNumber if case.CaseNumber is not None else '',
                    'Case Created on DateTime': case.Date if case.Date is not None else '',
                    'Case Reporter': case.CaseReporter.user_fk.name if case.CaseReporter and case.CaseReporter.user_fk and case.CaseReporter.user_fk.name is not None else '',
                    'Case Manager': case.CaseManager.user_fk.name if case.CaseManager and case.CaseManager.user_fk and case.CaseManager.user_fk.name is not None else '',
                    'Case TroubleShooter': case.CaseTroubleShooter.user_fk.name if case.CaseTroubleShooter and case.CaseTroubleShooter.user_fk and case.CaseTroubleShooter.user_fk.name is not None else '',
                    'Case Assigned to CR DateTime': case.Date if case.Date is not None else '',
                    'Case Assigned to CM DateTime': case.T1vrfDate if case.T1vrfDate is not None else '',
                    'Case Assigned to CT DateTime': case.T2vrfDate if case.T2vrfDate is not None else '',
                    'First Response sent by CT Date Time': case.T3vrfDate if case.T3vrfDate is not None else '',
                    'Resolved Datetime': case.ResolveTime if case.ResolveTime is not None else '',
                    'Closed Datetime': case.ClosingTime if case.ClosingTime is not None else '',
                    'Category': case.CaseCategory if case.CaseCategory is not None else '',
                    'Sub Category': case.SubCategory if case.SubCategory is not None else '',
                    })    
                    
            user_xlsx[userRole] = {'cases': case_data}





        print(user_xlsx,"Us33333er3")
    except Exception as e:
        traceback.print_exc()
        print("sddsdss",user_xlsx)
    return user_xlsx
def coallatecasescrcmct(queryset, **kwargs):
    operation=kwargs.get('operation', None)
    print(operation,"operattttion")
    if operation=="weekly":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        cases = Case.objects.filter(Date__range=(start_date, end_date),CurrentStatus__in=[CaseActiveStatus.DRAFT, CaseActiveStatus.UNREAD,CaseActiveStatus.NEW_CASE,CaseActiveStatus.READ])
        print(cases,"cccccases")
    elif operation=="monthly":
        start_date = datetime.now() - relativedelta(months=1)
        cases = Case.objects.filter(Date__range=(start_date, datetime.now()), CurrentStatus__in=[CaseActiveStatus.DRAFT, CaseActiveStatus.UNREAD,CaseActiveStatus.NEW_CASE,CaseActiveStatus.READ])
    casereporters={}
    casemanagers={}
    casetroubleshooters={}
    # link=
    for case in cases:
        # try:
        print(case)
        print((timezone.now() - case.Date)>= timedelta(days=3),"condiiii",case.CaseStatus==CaseStatus.ASSIGNED_TO_REPORTER,case.CaseDetails==None, case.CommentsByRep=="")
        # except Exception as e:
        #     traceback.print_exc()
        link="https://inache.co/CaseReport/"+str(case.id)
        print(link,"dasdsadsdsdsdsd")
        if case.CaseStatus==CaseStatus.ASSIGNED_TO_REPORTER:
            print("forstrument")
            # if case.CaseDetails==None or case.CommentsByRep==None:
            print("Adding")
            casereporter=case.CaseReporter
            if casereporter in casereporters:
                casereporters[casereporter].append(link)
            else:
                casereporters[casereporter] = [link]
        if case.CaseStatus==CaseStatus.ASSIGNED_TO_MANAGER and (datetime.now() - case.T1vrfDate) >= timedelta(days=3):
            if case.CommentsByMan==None:
                casemanager=case.CaseManager
                if casemanager in casemanagers:
                    casemanagers[casemanager].append(link)
                else:
                    casemanagers[casemanager] = [link]
        if (case.CaseStatus==CaseStatus.ASSIGNED_TO_TROUBLESHOOTER and (datetime.now() - case.T2vrfDate) >= timedelta(days=3)) or case.CaseStatus==CaseStatus.UNDER_INVESTIGATION and (datetime.now() - case.T3vrfDate) >= timedelta(days=3):
            casetroubleshooter=case.CaseTroubleShooter
            if casetroubleshooter in casetroubleshooters:
                casetroubleshooters[casetroubleshooter].append(link)
            else:
                casetroubleshooters[casetroubleshooter] = [link]
    print(casereporters,"Caserep")
    print(casemanagers,"casemanagers")
    print(casetroubleshooters,"casetroublesh")
    qset={'cr':casereporters,'cm':casemanagers,'ct':casetroubleshooters}
    print(qset,"casetroublesh")
    return qset

FUNCTION_MAPPINGS = {
    'check_recent_login': check_recent_login,
    'check_holiday': check_holiday,
    'SLADueDate':SLADueDateCalculation,
    'AwarenessProgram_Permission':AwarenessProgram_Permission,
    'xlsxforrasa':coallatecaserasafa,
    'collatecrcmct':coallatecasescrcmct,
    'POSH_Case_SMS_not_Sent':POSH_Case_SMS_not_Sent,
    'reminder_poshcases': reminder_poshcases,
    'check_action_after_worker_reply': check_action_after_worker_reply,
    'check_ra_case_closed': check_ra_case_closed,
    # Add more mappings as needed
}

