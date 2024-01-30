from django.db import models


class ReportingMedium(models.TextChoices):
    CALL = "Call"
    IN_PERSON = "In Person"
    SUGGESTION_BOX = "Suggestion Box"
    WORKER_COMMITTEE = "Worker Committee"


class CaseStatus(models.TextChoices):
    ASSIGNED_TO_REPORTER = "Assigned to Reporter"
    ASSIGNED_TO_MANAGER = "Assigned to Manager"
    ASSIGNED_TO_TROUBLESHOOTER = "Assigned to Troubleshooter"
    UNDER_INVESTIGATION = "Under Investigation"
    RESOLVED = "Resolved"
    RE_INVESTIGATION = "Re Investigation"
    CLOSED = "Closed"
    ASSIGNED_TO_QUALITY_CHECKER = "Assigned to Quality Checker"
    COMPLETED = "Completed"
    UNRESPONSIVE = "Unresponsive"
    APPROVED = "Approved"
    ASSIGNED_TO_REGIONAL_ADMIN = "Assigned to Regional Admin"
    RA_INVESTIGATION = "Investigation under Regional Admin"
    RE_INVESTIGATION_RA = "Regional Admin ReInvestigation"



class CaseNature(models.TextChoices):
    COMPLAIN = "Complaint"
    QUERY = "Query"
    SUGGESTION = "Suggestion"


class UserRole(models.TextChoices):
    CASE_REPORTER = "CR"
    CASE_MANAGER = "CM"
    CASE_TROUBLESHOOTER = "CT"
    FACTORY_ADMIN = "FACTORY_ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
    INACHE_ADMIN = "INACHE_ADMIN"
    REGIONAL_ADMIN = "REGIONAL_ADMIN"
    DEFAULT_ROLE = "DEFAULT_ROLE"


class Language(models.TextChoices):
    English = "English"
    Hindi = "Hindi"
    Kannada = "Kannada"
    Punjabi = "Punjabi"


class Region(models.TextChoices):
    NORTH = "North"
    SOUTH = "South"


class ConstantVars(models.TextChoices):
    INACHE = "IN"


class Gender(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    OTHERS = "Others"
    NOT_SPECIFIED = "Not Specified"


class Status(models.TextChoices):
    DRAFT = "Draft"
    SENT = "Sent"
    MODIFIED = "Modified"
    CTDRAFT = "CTDraft"


class ViewLogsIdentifier(models.TextField):
    ACKMSG = "ACKMSG"
    SENTMSG = "SENTMSG"
    REVERTMSG = "REVERTMSG"
    STATECHNG = "STATECHNG"
    VARCHANGED = "VARCHANGED"
    INVALIDATED = "INVALIDATED"
    VALIDATED = "VALIDATED"
    CLOSEMSG = "CLOSEMSG"


class CaseActiveStatus(models.TextChoices):
    DRAFT = "Draft"
    READ = "Read"
    UNREAD = "Unread"
    NEW_CASE = "new_cases"
    SUBMIT = "Submit"


class CaseType(models.TextChoices):
    NEW_CASES = "new_cases"
    IN_PROGRESS_CASES = "in_progress_cases"
    RESOLVED_CASES = "resolved_cases"
    CLOSED_CASES = "closed_cases"
    APPROVED_CASES = "approved_cases"


class UserResposibilities(models.TextChoices):
    CR = "Prepare Case Report. - Categorize the case. - Transfer the case to the Case Manager."
    CM = "Assessing Case Report prepared by CR. - Assign Case Report to the designated Case Troubleshooter."
    CT = "Assessing Case Report filled by CR & CM. - Seek information from workers/complainants for better resolution. - Resolve & Close case within the provided timeline."
    FACTORY_ADMIN = "Create/ Edit and Delete  CR, CM & CT. - Provide permission based access to CR, CM & CT. - Perform Other Miscellaneous activity. "


class ActionTypes(models.TextChoices):
    PRIORITY_PUT="Priority Updated - PUT"
    CASEVALIDATION_PUT="CaseValidation Updated - PUT"
    CASENATURE_PUT="CaseNature Updated - PUT"
    CASEFILE_PUT="Document Updated - PUT"
    CATEGORY_PUT="CaseCategory Updated - PUT"
    SUBCATEGORY_PUT="CaseSubCategory Updated - PUT"
    STATUS_PUT="CaseStatus Updated - PUT"
    CR_PUT="CaseReporter Assigned - PUT"
    CASE_RESOLVED_CT="Case Resolved by CT - POST"
    CASE_RESOLVED_RA="Case Resolved by RA - POST"
    CASE_CREATE="Case Uploaded - CREATE"
    CASE_ACK_MESSAGE_SENT="Acknowledgement Message Sent - POST"
    CASE_RESOLVING_MESSAGE_SENT="Case Resolving Message Sent - POST"
    CASE_REOPENED_SLA_BREACHED="Case Reopened - (New Case Made)- PUT"
    CASE_REOPENED_CT="Case Reopened - (ReInvestigation under CT) - PUT"
    CASE_REOPENED_RA="Case Reopened - (ReInvestigation under RA) - PUT"
    CASE_CLOSED="Case Closed - POST"
    CASE_UNRESPONSIVE="Case Unresponsive - POST"
    REVERT_MESSAGE="Revert Message from the Worker - POST"
    CT_FIRST_RESPONSE_SENT=" First Response Sent By CaseTroubleShooter - POST"
    RA_FIRST_RESPONSE_SENT=" First Response Sent By RegionalAdmin - POST"
    CASE_MESSAGE_SENT=" Case Message Sent - POST"
    CASE_MESSAGE_SENT_REPLY_REQUIRED = "Case Message Sent Where the Worker needs to Reply Back - POST"
    CM_ASSIGNED="Transferred to Case Manager - POST"
    CT_ASSIGNED="Transferred to Case Troubleshooter - POST"
    RA_ASSIGNED="Transferred to Regional Admin - POST"
    CASE_INVALID = "Case is Marked Invalid by Case Reporter - POST"
    UNCLEAR_MESSAGE_SENT = "Unclear Message Sent - POST"
    CASE_CLOSING_MESSAGE_SENT = "Case Closing Message Sent - POST"
    FOLLOWUP_MESSAGE_SENT = "Follow-up Message sent - POST"
    FOLLOWUP_MESSAGE_POSH_SENT_WRITTEN_COMPLAINT_RA = " Follow-up Message for written Complain Sent - POST"
    UNRESPONSIVE_MESSAGE_SENT = "Case Closed Due to Lack of Response, Message sent - POST"
    CASE_TRANSFERED = "Case Transfered to a different User - PUT"
    ROLE_TRANSFERED = "Role Transfered to a different User - PUT"
    CASE_TRANSFERED_SPLIT="Case Split to Multiple Users - PUT"
    CASE_TRANSFERED_MERGE="Case Merged - PUT"
    CASE_TRANSFERED_ASSIGN="Case Assigned - PUT"


class scheduleType(models.TextChoices):
    SEND_MESSAGE="Send Message"


