
import uuid
from accounts.models import Company, SNSTemplate
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def importawstemplates(request):
    templates =  [
   {
        'body': """
<div style="margin-top: 20px">
  <p>Dear {user_name},</p>

  <p>
    I hope this email finds you well. We wanted to inform you that a new case
    {case_number} has been assigned to you on Inache.
  </p>
  <p>
    You can access the case details, related documents, and any updates by
    logging into inache.co. We kindly request you to review the case details and
    begin working on it at your earliest convenience. Your prompt attention to
    this case is greatly appreciated. We look forward to your diligent efforts
    in resolving this matter effectively.
  </p>
  <p>
    Thank you for your dedication to our team and your commitment to providing
    exceptional service to our clients.
  </p>
  <p>
    Best regards,<br />
    Inache
  </p>
</div>
""",
        'subject': "{case_number} Assigned to You on Inache",
        'title': "Any New Case Assigned",
        'variables': {"user_name": "user_name", "case_number": "case_number"},
        'language': "English",
        'company_fk': 1,
        'template_category': "Email"
    },
    {
        'body': """<div style="margin-top: 20px">
  <p>Dear {user_name},</p>

  <p>
    I hope this message finds you well. We wanted to bring to your attention a
    critical matter regarding a pending case on Inache.
  </p>
  <p>
    We have a case with the following details that is currently on the verge of
    breaching its SLA within the next 24 hours:
  </p>
  <p>
    Case ID: {case_number}<br />
    Assigned To: {user_name}<br />
    SLA Due: {sla_due_date_and_time}
  </p>
  <p>
    However, it seems that the Case Report has not been filled in the system yet.
    It is crucial that we document the case related updates in the Case Report to
    ensure transparency and effective communication with the complainant.
  </p>
  <p>
    I kindly request you to urgently update the Case Report with the latest
    information. This will not only help us manage the case efficiently but also
    prevent an SLA breach.
  </p>
  <p>
    Thank you for your immediate attention to this issue.
  </p>
  <p>
    Best regards,<br />
    Inache
  </p>
</div>
""",
        'subject': "Urgent: Case {case_number} SLA Breach Warning",
        'title': "Any Case that is about to breach its SLA in the next 24 hrs and Case Report is not filled",
        'variables': {"user_name": "user_name", "case_number": "case_number", "sla_due_date_and_time": "sla_due_date_and_time"},
        'language': "English",
        'company_fk': 1,
        'template_category': "Email"
    },
    {
        'body': """<div style="margin-top: 20px">
  <p>Dear {user_name},</p>

  <p>
    I trust you are well. I'm writing to remind you about a pending case report
    draft on Inache.
  </p>
  <p>
    Case ID: {case_number}<br />
    Report Draft Status: Pending
  </p>
  <p>
    It appears that the case report for the above-mentioned case is still in
    draft status. Completing and submitting the report is essential for
    maintaining accurate records and facilitating effective communication with
    the complainant.
  </p>
  <p>
    Your cooperation in this matter is greatly appreciated. Let's work together
    to ensure our worker's well being.
  </p>
  <p>
    Thank you for your prompt attention.
  </p>
  <p>
    Best regards,<br />
    Inache
  </p>
</div>
""",
        'subject': "Action Required: Pending Case {case_number} Report Draft",
        'title': "Any Case Report that is in Draft",
        'variables': {"user_name": "user_name", "case_number": "case_number"},
        'language': "English",
        'company_fk': 1,
        'template_category': "Email"
    },
    {
        'body': """<div style="margin-top: 20px">
  <p>Dear {user_name},</p>

  <p>
    I hope this message finds you well. We wanted to inform you that a response
    has been received regarding Case {case_number} on Inache from the complainant.
  </p>
  <p>
    You can log in inache.co to hear complete voice note by going into the view
    logs of the Case {case_number}.
  </p>
  <p>
    Best regards,<br />
    Inache
  </p>
</div>
""",
        'subject': "Response Received: Case {case_number}",
        'title': "Reply received from a worker",
        'variables': {"user_name": "user_name", "case_number": "case_number"},
        'language': "English",
        'company_fk': 1,
        'template_category': "Email"
    },
    {
        'body': """<div style="margin-top: 20px">
  <p>Dear {user_name},</p>

  <p>
    I hope you're doing well. We wanted to bring to your attention the status of
    some cases that require your immediate attention on Inache. These cases have
    been left unattended for more than 3 days and fall into the following
    categories:
  </p>
  <p>
    <strong>Unread Cases:</strong>
  </p>
  <p>
    Case Count - Total number of Unread cases<br />
    Status: Unread
  </p>
  <p>
    <strong>Cases Without Filled Case Report:</strong>
  </p>
  <p>
    Case Count - Total number of Unread cases<br />
    Status: Pending Case Report
  </p>
  <p>
    <strong>Cases in Draft Status:</strong>
  </p>
  <p>
    Case Count - Total number of Unread cases<br />
    Status: Draft
  </p>
  <p>
    Please log in to Inache using the following link to access these cases and
    take the necessary actions:
  </p>
  <p>
    {collated_link_to_cases}
  </p>
  <p>
    Your prompt attention to these cases is crucial in maintaining efficient
    grievance resolution and worker well being. We appreciate your efforts in
    resolving these pending matters.
  </p>
  <p>
    Best regards,<br />
    Inache
  </p>
</div>
""",
        'subject': "Attention Required: Weekly Pending Cases Requiring Action",
        'title': "Collated link of Cases that were left unread, without filling Case Report or in Draft, along with Status, for cases that were unattended for more than 3 days. (Weekly)",
        'variables': {"user_name": "user_name", "collated_link_to_cases": "collated_link_to_cases"},
        'language': "English",
        'company_fk': 1,
        'template_category': "Email"
    },
    {
        'body': """<div style="margin-top: 20px">
  <p>Dear {user_name},</p>

  <p>
    I trust this message finds you well. We would like to draw your attention to
    a critical matter regarding certain cases on Inache. Unfortunately, these
    cases have remained unattended for over a month and require your immediate
    attention.
  </p>
  <p>
    Here is a collated link to the cases along with their respective statuses:
  </p>
  <p>
    {collated_link_to_overdue_cases}
  </p>
  <p>
    The following categories of cases are involved:
  </p>
  <p>
    <strong>Unread Cases:</strong>
  </p>
  <p>
    Case Count - Total Number of Unread Cases<br />
    Status: Unread
  </p>
  <p>
    <strong>Cases Without Filled Case Report:</strong>
  </p>
  <p>
    Case Count - Total Number of Unread Cases<br />
    Status: Pending Case Report
  </p>
  <p>
    <strong>Cases in Draft Status:</strong>
  </p>
  <p>
    Case Count - Total Number of Unread Cases<br />
    Status: Draft
  </p>
  <p>
    Given the extended period of inactivity, we urgently request you to review
    and address these cases. Your timely intervention will help us maintain our
    commitment to resolving grievances promptly and effectively. Your proactive
    engagement in resolving these overdue cases is greatly appreciated.
  </p>
  <p>
    Thank you for your immediate attention to this matter.
  </p>
  <p>
    Best regards,<br />
    Inache
  </p>
</div>
""",
        'subject': "Urgent Action Required: Monthly Overdue Cases Requiring Immediate Attention",
        'title': "Monthly",
        'variables': {"user_name": "user_name", "collated_link_to_overdue_cases": "collated_link_to_overdue_cases"},
        'language': "English",
        'company_fk': 1,
        'template_category': "Email"
    },
    {
    'body': """<div style="margin-top: 20px">
  <p>Dear {user_name},</p>

  <p>
    I hope this message finds you well. I wanted to inform you about recent
    changes that have occurred in the case assignment due to split/merge actions
    carried out by the Super Admin/Factory Admin.
  </p>
  <p>
    As a result of these actions, certain cases have been reassigned or
    redistributed. Please log in to the system to access your updated list of
    assigned cases. Kindly review the details and ensure that you are aware of
    your new responsibilities.
  </p>
  <p>
    Thank you for your understanding and cooperation as we work to optimize our
    case management processes.
  </p>
  <p>
    Best regards,<br />
    Inache
  </p>
</div>
""",
    'subject': "Update: Changes to Your Assigned Cases",
    'title': "Cases assigned to a Case Reporter when Split or Merge happened for a user by Super Admin or Factory Admin",
    'variables': {"user_name": "user_name"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
  <p>Dear {user_name},</p>

  <p>
    I trust this email finds you well. We are writing to inform you about a
    recent change in your access role within our system.
  </p>
  <p>
    Effective {date_today}, your access role has been updated from
    {previous_role} to {new_role}.
  </p>
  <p>
    With your new access role, you will have access to
    {a_brief_description_of_new_access_privileges}.
  </p>
  <p>
    Please take a moment to review your new access privileges and ensure that
    you have the necessary permissions to carry out your tasks seamlessly on
    Inache.
  </p>
  <p>
    We appreciate your understanding and cooperation in this matter. Your
    continued dedication to maintaining the security and integrity of our
    systems is invaluable.
  </p>
  <p>
    Thank you for your attention to this notification.
  </p>
  <p>
    Best regards,<br />
    Inache
  </p>
</div>
""",
    'subject': "Access Role Change Notification",
    'title': "Access Change from One Role to Another",
    'variables': {"user_name": "user_name", "date_today": "date_today", "previous_role": "previous_role", "new_role": "new_role", "a_brief_description_of_new_access_privileges": "a_brief_description_of_new_access_privileges"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
  <p>Dear {user_name},</p>

  <p>
    We hope you are doing well. We're excited to share an opportunity for you
    to contribute to our factory's improvement and awareness initiatives.
  </p>
  <p>
    Did you know that you can now conduct an Awareness Program for our workers
    using Inache? This powerful tool not only helps in addressing grievances
    but can also be used to educate and create awareness among our workforce.
  </p>
  <p>
    You can leverage the dashboard to:
  </p>
  <ul>
    <li>Share Updates: Use the dashboard to communicate updates,
      improvements, and company policies directly to the workers.</li>
    <li>Conduct Inache Training: Create informative presentations to educate our
      workers about Inache.</li>
  </ul>
  <p>
    To get started, simply log in to Inache and explore its features.
  </p>
  <p>
    {awarenessProgram_video}
  </p>
  <p>
    Your proactive engagement in enhancing awareness and communication is
    highly appreciated. Together, we can build a safer, more informed, and
    productive work environment.
  </p>
  <p>
    Thank you for being an integral part of our efforts.
  </p>
  <p>
    Best regards,<br />
    Inache
  </p>
</div>
""",
    'subject': "Empowering You: Conduct Awareness Program Using Inache",
    'title': "New Access Provided for Awareness Program (CR & CT)",
    'variables': {"user_name": "user_name", "awarenessProgram_video": "awarenessProgram_video"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
    },
    {
    'body': """<div style="margin-top: 20px">
  <p>Dear {user_name},</p>

  <p>
    Greetings! We wanted to gently remind you about the ongoing initiative to
    conduct Awareness Programs for our factory workforce. Your contribution in
    educating and enlightening our team is highly valued.
  </p>
  <p>
    As of now, here's a quick overview of the Awareness Programs scheduled for
    this month compared to the number of programs conducted:
  </p>
  <ul>
    <li>Scheduled Awareness Programs for the Month: {scheduled_awarenessPrograms}</li>
    <li>Completed Awareness Programs: {completed_awarenessPrograms}</li>
    <li>Pending Awareness Programs : {pending_awarenessPrograms}</li>
  </ul>
  <p>
    We encourage you to continue your efforts in organizing these programs to
    ensure that workers stay well-informed and engaged about the usage of
    Inache. Your dedication to this initiative greatly influences our work
    environment and safety practices.
  </p>
  <p>
    Thank you for your commitment, and looking forward to seeing the positive
    outcomes of your efforts.
  </p>
  <p>
    Best regards,<br />
    Inache
  </p>
</div>
""",
    'subject': "Friendly Reminder: Conducting Awareness Programs",
    'title': "Conducting Awareness Program (If user has access to Awareness program)",
    'variables': {"user_name": "user_name", "scheduled_awarenessPrograms": "scheduled_awarenessPrograms", "completed_awarenessPrograms": "completed_awarenessPrograms", "pending_awarenessPrograms": "pending_awarenessPrograms"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
{
    
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>

<p>
    I hope this email finds you well. We are writing to inform you about a recent
    change in your system access.
</p>
<p>
    Effective immediately, your access to Inache as {role} has been revoked.
</p>
<p>
    We understand that this change may impact your work, and we are here to
    assist you during this transition. If you believe this access revocation is
    in error, please don't hesitate to reach out to Factory Admin/Super Admin.
</p>
<p>
    Thank you for your understanding and cooperation. We apologize for any
    inconvenience this may cause and appreciate your prompt attention to this
    matter.
</p>
<p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Important Notice: Access Revoked",
    'title': "When Access is Revoked",
    'variables': {"user_name": "user_name", "role": "role"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """
    <div style="margin-top: 20px">
     <p>Dear {factory_unit_number},</p>
    
    <p>
        I am thrilled to share some fantastic news with you all. {factory_unit_number}
        has emerged as the winner of this month's incentive cycle! This achievement
        is a testament to your hard work, dedication, and commitment to excellence.
    </p>
    <p>
        Your efforts have not only contributed to our success but also set a
        remarkable example for everyone in the organization. Your determination
        and teamwork are truly inspiring.
    </p>
    <p>
        Let's take a moment to celebrate this well-deserved victory. Your consistent
        performance continues to drive us forward, and we look forward to achieving
        even greater milestones together.
    </p>
    <p>Congratulations once again, and keep up the outstanding work!</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Congratulations on Winning the Monthly Incentive Cycle!",
    'title': "Congratulations Mail if Factory was Winner of Monthly Incentive Cycle",
    'variables': {"factory_unit_number": "factory_unit_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},

    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {factory_unit_number},</p>
    <p>
        I hope this email finds you well. As we reach the midpoint of the current
        incentive cycle, I wanted to provide you with a quick update on the status
        of your eligibility for the Incentive Program.
    </p>
    <p>
        Here's a brief overview of where we stand:
    </p>
    <p>
        Minimum Compliance factory Required for Eligibility: {minimum_compliance_percentage}
    </p>
    <p>
        Table with T0, T1, T2, T3a1, T3a2, T3b1, T3b2, T3c1, T3c2.
    </p>
    <p>
        Adhered Compliance Factor Percentage -
    </p>
    <p>
        -Table with T0, T1, T2, T3a1, T3a2, T3b1, T3b2, T3c1, T3c2.
    </p>
    <p>
        Minimum Awareness Program to be conducted
    </p>
    <p>
        No of Awareness program conducted -
    </p>
    <p>
        Pending Awareness program-
    </p>
    <p>
        We're excited to see the progress you've made so far. Keep up the great
        work and continue to aim for your goals! If you have any questions or need
        clarification about the program's criteria or your current status, feel
        free to reach out to our support team at {support_contact_no}.
    </p>
    <p>
        Remember, your dedication and efforts make a significant impact, and
        we're here to support you every step of the way.
    </p>
    <p>Thank you for your commitment to excellence.</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Bi-Weekly Incentive Program Eligibility Update",
    'title': "Status of the Eligibility for the Incentive Program",
    'variables': {"factory_unit_number": "factory_unit_number", "minimum_compliance_percentage": "minimum_compliance_percentage", "support_contact_no": "support_contact_no"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name}</p>
    <p>
        We are pleased to inform you that you have been assigned a new role on
        Inache.
    </p>
    <p>
        As part of the CR of {factory_unit_number}, you will be responsible for:
    </p>
    <ul>
        <li>Prepare Case Report.</li>
        <li>Categorize the case.</li>
        <li>Transfer the case to the Case Manager.</li>
    </ul>
    <p>
        We believe that you have the skills and expertise required to excel in
        this role, and we are excited to have you on board.
    </p>
    <p>
        We welcome you to our Inache family as a CR. We look forward to working
        with you to make a difference in our community.
    </p>
    <p>
        Note - Please use your current email.id and Password to log into Inache.
    </p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Welcome to Inache as CR of {factory_unit_number}",
    'title': "Access for a new user as CR in same/different factory (In Case of Multi Role access)",
    'variables': {"factory_unit_number": "factory_unit_number", "user_name": "user_name"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name}</p>
    <p>
        We are pleased to inform you that you have been assigned a new role on
        Inache.
    </p>
    <p>
        As part of the CM of {factory_unit_number}, you will be responsible for:
    </p>
    <ul>
        <li>Assessing Case Report prepared by CR.</li>
        <li>Assign the Case Report to the designated Case Troubleshooter.</li>
    </ul>
    <p>
        We believe that you have the skills and expertise required to excel in
        this role, and we are excited to have you on board.
    </p>
    <p>
        We welcome you to our Inache family as a CM. We look forward to working
        with you to make a difference in our community.
    </p>
    <p>
        Note - Please use your current email.id and Password to log into Inache.
    </p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Welcome to Inache as CM of {factory_unit_number}",
    'title': "Access for a new user as CM in same/different factory (In Case of Multi Role access)",
    'variables': {"factory_unit_number": "factory_unit_number", "user_name": "user_name"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
}
,
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name}</p>
    <p>
        We are pleased to inform you that you have been assigned a new role on
        Inache.
    </p>
    <p>
        As part of the CT of {factory_unit_number}, you will be responsible for:
    </p>
    <ul>
        <li>Assessing Case Report filled by CR & CM.</li>
        <li>Seeking information from workers/complainants for better resolution.</li>
        <li>Resolving & Closing cases within the provided timeline.</li>
    </ul>
    <p>
        We believe that you have the skills and expertise required to excel in
        this role, and we are excited to have you on board.
    </p>
    <p>
        We welcome you to our Inache family as a CT. We look forward to working
        with you to make a difference in our community.
    </p>
    <p>
        Note - Please use your current email.id and Password to log into Inache.
    </p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Welcome to Inache as CT of {factory_unit_number}",
    'title': "Access for a new user as CT in same/different factory (In Case of Multi Role access)",
    'variables': {"factory_unit_number": "factory_unit_number", "user_name": "user_name"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
  
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I hope this email finds you well. As part of our ongoing efforts to keep
        you informed about the status of cases, I'm pleased to share with you the
        monthly collated cases report.
    </p>
    <p>
        Attached to this email is an Excel spreadsheet (xlsx) containing the
        following details for each case:
    </p>
    <ul>
        <li>Case Number</li>
        <li>Priority</li>
        <li>Assigned To</li>
        <li>Assigned On Date</li>
        <li>SLA Breached Status</li>
    </ul>
        {link_to_xlsx_file_for_monthly_collated_cases}
    <p>
        This report offers a comprehensive overview of the cases currently being
        handled, their assigned priorities, the responsible individuals, and the
        status of SLA breaches.
    </p>
    <p>Please review this report at your convenience.</p>
    <p>Thank you for your continued involvement in our processes.</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Monthly Collated Cases Report and Status Update",
    'title': "When Critical Case is Closed",
    'variables': {"user_name": "user_name"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I hope this message finds you well. We have a critical matter that
        requires your immediate attention. The case {case_number} assigned to you
        with a high-priority status is still pending due to an incomplete case
        report.
    </p>
    <p>
        Given the urgency of the situation, we urge you to fill out the case
        report as soon as possible on Inache. Timely documentation is essential
        for effective communication and resolution.
    </p>
    <ul>
        <li>Case ID: {case_number}</li>
        <li>Priority: High</li>
        <li>Status: Pending Case Report</li>
    </ul>
    <p>
        Your swift action will help us ensure that the necessary steps are taken
        to address this case promptly and efficiently.
    </p>
    <p>
        Thank you for your immediate attention to this matter. We appreciate
        your commitment to maintaining the quality of our case management process.
    </p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "URGENT: Pending Case Report for High-Priority Case",
    'title': "If Case Report is not filled and Case is of High Priority",
    'variables': {"user_name": "user_name", "case_number": "case_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        Greetings! We are writing to remind you about a case {case_number} that
        is currently pending due to an incomplete case report on Inache. The case
        is of medium priority and requires your attention.
    </p>
    <ul>
        <li>Case ID: {case_number}</li>
        <li>Priority: Medium</li>
        <li>Status: Pending Case Report</li>
    </ul>
    <p>
        Completing the case report is crucial for maintaining accurate records
        and ensuring a smooth resolution process. Your timely action will help us
        provide the best possible service to our clients and stakeholders.
    </p>
    <p>Thank you for your prompt attention to this matter.</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Reminder: Pending Case Report for Medium-Priority Case",
    'title': "If Case Report is not filled and Case is of Medium Priority",
    'variables': {"user_name": "user_name", "case_number": "case_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I hope this message finds you well. I wanted to bring to your attention
        a case {case_number} that is still awaiting completion of the case
        report on Inache. The case is currently categorized as low priority.
    </p>
    <ul>
        <li>Case ID: {case_number}</li>
        <li>Priority: Low</li>
        <li>Status: Pending Case Report</li>
    </ul>
    <p>
        While the priority might be lower, completing the case report is
        essential for maintaining accurate documentation and ensuring a
        comprehensive resolution process.
    </p>
    <p>
        I kindly request you to review the case details and fill out the case
        report at your earliest convenience.
    </p>
    <p>
        Thank you for your attention to this matter. Your dedication to our case
        management process is greatly appreciated.
    </p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Reminder: Pending Case Report for Low-Priority Case",
    'title': "If Case Report is not filled and Case is of Low Priority",
    'variables': {"user_name": "user_name", "case_number": "case_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I hope this message finds you well. We have a critical matter that
        requires your immediate attention. The case {case_number} assigned to
        you with a high-priority status is still pending due to an incomplete
        case report.
    </p>
    <ul>
        <li>Case ID: {case_number}</li>
        <li>Priority: High</li>
        <li>Status: Pending Case Report</li>
    </ul>
    <p>
        Given the urgency of the situation, we urge you to fill out the case
        report as soon as possible on Inache. Timely documentation is essential
        for effective communication and resolution.
    </p>
    <p>
        Your swift action will help us ensure that the necessary steps are
        taken to address this case promptly and efficiently.
    </p>
    <p>
        Thank you for your immediate attention to this matter. We appreciate
        your commitment to maintaining the quality of our case management
        process.
    </p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "URGENT: Pending Case Report for High-Priority Case",
    'title': "If Case Report is not filled and Case is of High Priority",
    'variables': {"user_name": "user_name", "case_number": "case_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        Greetings! We are writing to remind you about a case {case_number}
        that is currently pending due to an incomplete case report on Inache.
        The case is of medium priority and requires your attention.
    </p>
    <ul>
        <li>Case ID: {case_number}</li>
        <li>Priority: Medium</li>
        <li>Status: Pending Case Report</li>
    </ul>
    <p>
        Completing the case report is crucial for maintaining accurate records
        and ensuring a smooth resolution process. Your timely action will help
        us provide the best possible service to our clients and stakeholders.
    </p>
    <p>Thank you for your prompt attention to this matter.</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Reminder: Pending Case Report for Medium-Priority Case",
    'title': "If Case Report is not filled and Case is of Medium Priority",
    'variables': {"user_name": "user_name", "case_number": "case_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I hope this message finds you well. I wanted to bring to your
        attention a case {case_number} that is still awaiting completion of
        the case report on Inache. The case is currently categorized as low
        priority.
    </p>
    <ul>
        <li>Case ID: {case_number}</li>
        <li>Priority: Low</li>
        <li>Status: Pending Case Report</li>
    </ul>
    <p>
        While the priority might be lower, completing the case report is
        essential for maintaining accurate documentation and ensuring a
        comprehensive resolution process.
    </p>
    <p>
        I kindly request you to review the case details and fill out the case
        report at your earliest convenience.
    </p>
    <p>
        Thank you for your attention to this matter. Your dedication to our
        case management process is greatly appreciated.
    </p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Reminder: Pending Case Report for Low-Priority Case",
    'title': "If Case Report is not filled and Case is of Low Priority",
    'variables': {"user_name": "user_name", "case_number": "case_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I hope this email finds you well. I wanted to bring to your attention
        a recurring issue we've been facing with our API for uploading worker
        data. Unfortunately, we have experienced another failure this month,
        which has prevented us from automatically updating the worker data.
    </p>
    <p>
        In order to ensure that we maintain accurate and up-to-date records,
        please go to the Edit Factory Screen and upload workers' data in CSV
        format.
    </p>
    <p>
        We understand that this is an inconvenience, and we apologize for any
        disruption this may cause. Rest assured, we are actively working on
        resolving the API issue to prevent any future interruptions.
    </p>
    <p>Thanks for your cooperation.</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Monthly Worker Data Upload Request",
    'title': "For Uploading New Worker's Data every Month (in case of API Failure)",
    'variables': {"user_name": "user_name"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I hope this email finds you well. We would like to bring to your
        attention a new case related to the Prevention of Sexual Harassment
        (POSH) policy that has landed on the dashboard under your jurisdiction.
    </p>
    <p>
        <strong>Case ID:</strong> {case_number}<br />
        <strong>Date Received:</strong> {case_received_date}<br />
        <strong>Priority:</strong> {case_priority_level}
    </p>
    <p>
        As the Regional Admin, your role is vital in ensuring that all POSH
        cases are handled promptly and in accordance with the established
        protocols. We kindly request your immediate attention to this matter.
    </p>
    <p>
        Please review the case details and take the necessary steps to
        initiate the appropriate actions.
    </p>
    <p>
        Your swift response is crucial in upholding our commitment to
        providing a safe and respectful work environment for all employees.
    </p>
    <p>Thank you for your dedication to this important aspect of our organizational culture.</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "New POSH Case Alert: Immediate Action Required Case {case_number}",
    'title': "When Critical Case like POSH and Special cases landed on the Dashboard",
    'variables': {"user_name": "user_name", "case_number": "case_number", "case_received_date": "case_received_date", "case_priority_level": "case_priority_level"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I trust this email finds you well. I'm writing to bring a critical
        matter to your attention. A new special case has landed on the
        dashboard that requires immediate attention and your expertise.
    </p>
    <p>
        <strong>Case ID:</strong> {case_number}<br />
        <strong>Date Received:</strong> {case_received_date}<br />
        <strong>Priority:</strong> {case_priority_level}
    </p>
    <p>
        Given the unique nature of this case and its potential impact, your
        guidance and decision-making are crucial. Should you require any
        additional information or support, please do not hesitate to reach
        out to us. Your swift intervention will greatly contribute to the
        efficient resolution of this special case.
    </p>
    <p>Thank you for your prompt attention to this matter.</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "New Special Case Alert: Immediate Attention Required Case {case_number}",
    'title': "Special Case",
    'variables': {"user_name": "user_name", "case_number": "case_number", "case_received_date": "case_received_date", "case_priority_level": "case_priority_level"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I hope this email finds you well. I am writing to remind you about the
        pending action regarding the POSH case {case_number} assigned to you. The
        case report for this POSH case has not been opened within the
        stipulated 24-hour window or has been kept in draft status.
    </p>
    <p>
        As a crucial part of our policy and compliance, timely completion of
        the case report is essential. It not only ensures accurate
        documentation but also facilitates effective case resolution and
        reporting.
    </p>
    <p>
        We kindly request you to promptly open the case report or finalize
        the draft, as applicable.
    </p>
    <p>
        Your immediate attention to this matter is greatly appreciated.
        Ensuring compliance with our policies reflects our commitment to
        maintaining a safe and inclusive work environment.
    </p>
    <p>Thank you for your cooperation.</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Urgent Reminder: Pending Action Required on POSH Case Report Case {case_number}",
    'title': "If the Case report of Critical Cases (POSH & Special cases) were not opened within 24hrs or kept in Draft",
    'variables': {"user_name": "user_name", "case_number": "case_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I trust this email finds you well. I wanted to bring to your attention
        a critical matter regarding the special case {case_number} assigned to
        you. The case report for this special case has not been opened within
        the designated 24-hour timeframe or has been kept in draft status.
    </p>
    <p>
        As a special case often demands immediate attention and exceptional
        care, timely completion of the case report is of utmost importance.
        This ensures that the details and actions taken are documented
        accurately and effectively.
    </p>
    <p>
        I kindly urge you to open the case report or finalize the draft
        without further delay.
    </p>
    <p>
        Your swift response is crucial in addressing this matter. Your
        dedication to our processes ensures that we provide exceptional
        service and maintain transparency in our operations and with our
        workforce.
    </p>
    <p>Thank you for your understanding and cooperation.</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Urgent Reminder: Pending Action Required on Special Case Report Case {case_number}",
    'title': "If the Case report of Critical Cases (POSH & Special cases) were not opened within 24hrs or kept in Draft",
    'variables': {"user_name": "user_name", "case_number": "case_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I trust this email finds you well. I am writing to inform you that
        the critical case {case_number} which you were closely monitoring has
        been successfully resolved and closed.
    </p>
    <p>Here are the key details:</p>
    <ul>
        <li><strong>Case ID:</strong> {case_number}</li>
        <li><strong>Status:</strong> Closed</li>
    </ul>
    <p>
        The collaborative efforts of the team, including your valuable input,
        played a significant role in reaching a successful resolution. Your
        commitment to addressing critical matters is truly commendable.
    </p>
    <p>Thank you for your attention to this important matter.</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Case Closed: Critical Matter Resolved",
    'title': "When Critical Case is Closed",
    'variables': {"user_name": "user_name", "case_number": "case_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I hope this email finds you well. As part of our ongoing efforts to
        keep you informed about the status of cases, I'm pleased to share
        with you the weekly collated cases report.
    </p>
    <p>
        Attached to this email is an Excel spreadsheet (xlsx) containing
        the following details for each case:
    </p>
    <ul>
        <li>Case Number</li>
        <li>Priority</li>
        <li>Assigned To</li>
        <li>Assigned On Date</li>
        <li>SLA Breached Status</li>
    </ul>
    {xlxs}
    <p>
        This report offers a comprehensive overview of the cases currently
        being handled, their assigned priorities, the responsible individuals,
        and the status of SLA breaches.
    </p>
    <p>Please review this report at your convenience.</p>
    <p>Thank you for your continued involvement in our processes.</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Weekly Collated Cases Report and Status Update",
    'title': "Collated Cases every weekly basis with a xlsx attached showing Case Number, Priority and Assigned to, Assigned on Date, SLA Breached Status.",
    'variables': {"user_name": "user_name", "xlxs":"xlxs"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I hope this email finds you well. As part of our ongoing efforts to
        keep you informed about the status of cases, I'm pleased to share
        with you the monthly collated cases report.
    </p>
    <p>
        Attached to this email is an Excel spreadsheet (xlsx) containing
        the following details for each case:
    </p>
    <ul>
        <li>Case Number</li>
        <li>Priority</li>
        <li>Assigned To</li>
        <li>Assigned On Date</li>
        <li>SLA Breached Status</li>
    </ul>
    {xlxs}
    <p>
        This report offers a comprehensive overview of the cases currently
        being handled, their assigned priorities, the responsible individuals,
        and the status of SLA breaches.
    </p>
    <p>Please review this report at your convenience.</p>
    <p>Thank you for your continued involvement in our processes.</p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Monthly Collated Cases Report and Status Update",
    'title': "Collated Cases every  Monthly basis with a xlsx attached showing Case Number, Priority and Assigned to, Assigned on Date, SLA Breached Status.",
    'variables': {"user_name": "user_name", "xlxs": "xlxs"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
    {
    'body': """<div style="margin-top: 20px">
    <p>Dear {user_name},</p>
    <p>
        I hope you are doing well. We would like to remind you about the
        importance of keeping our holiday calendar up-to-date on Inache.
    </p>
    <p>
        As we approach the upcoming months, accurate holiday information is
        crucial for effective planning and communication. You have the option
        to either update the holiday calendar manually or utilize the convenient
        bulk upload feature.
    </p>
    <p>
        Here's a quick guide to both options:
    </p>
    <strong>Option 1: Manual Update</strong>
    <ol>
        <li>Log in to the Grievance Redressal System.</li>
        <li>Navigate to the Holiday Calendar section.</li>
        <li>Add or edit individual holiday entries as needed.</li>
    </ol>
    <strong>Option 2: Bulk Upload</strong>
    <ol>
        <li>Prepare a spreadsheet with the holiday details (date, name, etc.).</li>
        <li>Log in to the Grievance Redressal System.</li>
        <li>Access the Bulk Upload feature in the Holiday Calendar section.</li>
        <li>Follow the prompts to upload the prepared spreadsheet.</li>
    </ol>
    <p>
        By keeping the holiday calendar accurate and current, we ensure that
        our workforce is well-informed and that our operations run smoothly.
        Your attention to this matter is greatly appreciated.
    </p>
    <p>
        Thank you for your dedication to maintaining clear communication within
        the organization.
    </p>
    <p>Best regards,<br />Inache</p>
</div>
""",
    'subject': "Reminder: Update Holiday Calendar or Use Bulk Upload Feature",
    'title': "For Uploading Holiday Calendar (Reminder Email)",
    'variables': {"user_name": "user_name"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
}
# need to fill variables 
,{
    'body': """<div style="margin-top: 20px;">
    <p>Dear {user_name},</p>
  
    <p>
      We are pleased to onboard you as a Case Reporter on Inache.
    </p>
  
    <p>
      To get started with your new role, follow the steps below:
    </p>
  
    <ol>
      <li>Click on the following link to create a new password {password_reset_link}</li>
      <li>Create a strong password.</li>
      <li>Confirm your new Password.</li>
    </ol>
  
    <p>
      Note: The password reset link will only be accessible for 2 days.
    </p>
  
    <p>
      As part of the CR of {factory_unit_number}, you will be responsible for:
    </p>
  
    <ul>
      <li>Prepare Case Report.</li>
      <li>Categorize the case.</li>
      <li>Transfer the case to the Case Manager.</li>
    </ul>
  
    <p>
      We believe you have the skills and expertise required to excel in this
      role, and we are excited to have you on board.
    </p>
  
    <p>Best Regards,</p>
  
    <p>Inache</p>
  </div>
  
""",
    'subject': "Welcome to Inache as a Case Reporter",
    'title': "First-time Onboarding Mail for CR",
    'variables': {"user_name": "user_name","factory_unit_number":"factory_unit_number", "password_reset_link":"password_reset_link"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
}  
,{
    'body': """<div style="margin-top: 20px;">
    <p>Dear {user_name},</p>
  
    <p>
      We are pleased to onboard you as a Case Manager on Inache.
    </p>
  
    <p>
      To get started with your new role, follow the steps below:
    </p>
  
    <ol>
      <li>Click on the following link to create a new password {password_reset_link}</li>
      <li>Create a strong password.</li>
      <li>Confirm your new Password.</li>
    </ol>
  
    <p>
      Note: The password reset link will only be accessible for 2 days.
    </p>
  
    <p>
      As part of the CM of {factory_unit_number}, you will be responsible for:
    </p>
  
    <ul>
      <li>Assessing Case Report prepared by Case Reporter.</li>
      <li>Assigning the Case Report to the designated Case Troubleshooter.</li>
    </ul>
  
    <p>
      We believe you have the skills and expertise required to excel in this
      role, and we are excited to have you on board.
    </p>
  
    <p>Best Regards,</p>
  
    <p>Inache</p>
  </div>
  
""",
    'subject': "Welcome to Inache as a Case Manager",
    'title': "First-time Onboarding Mail for CM",
    'variables': {"user_name": "user_name","factory_unit_number":"factory_unit_number", "password_reset_link":"password_reset_link"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
{
    'body': """<div style="margin-top: 20px;">
    <p>Dear {user_name},</p>
  
    <p>
      We are pleased to onboard you as a Case Troubleshooter on Inache.
    </p>
  
    <p>
      To get started with your new role, follow the steps below:
    </p>
  
    <ol>
      <li>Click on the following link to create a new password {password_reset_link}</li>
      <li>Create a strong password.</li>
      <li>Confirm your new Password.</li>
    </ol>
  
    <p>
      Note: The password reset link will only be accessible for 2 days.
    </p>
  
    <p>
      As part of the CT of {factory_unit_number}, you will be responsible for:
    </p>
  
    <ul>
      <li>Assessing Case Report filled by CR & CM.</li>
      <li>Seeking information from workers/complainants for better resolution.</li>
      <li>Resolving and Closing the case within the provided timeline.</li>
    </ul>
  
    <p>
      We believe you have the skills and expertise required to excel in this
      role, and we are excited to have you on board.
    </p>
  
    <p>Best Regards,</p>
  
    <p>Inache</p>
  </div>
""",
    'subject': "Welcome to Inache as a Case Troubleshooter",
    'title': "First-time Onboarding Mail for CT",
    'variables': {"user_name": "user_name","factory_unit_number":"factory_unit_number", "password_reset_link":"password_reset_link"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
{
    'body': """<div style="margin-top: 20px;">
    <p>Dear {user_name},</p>
  
    <p>
      We are pleased to inform you that you have been assigned a new role to you
      on Inache.
    </p>
  
    <p>
      As part of the CR of {factory_unit_number}, you will be responsible for:
    </p>
  
    <ul>
      <li>Prepare Case Report.</li>
      <li>Categorize the case.</li>
      <li>Transfer the case to the Case Manager.</li>
    </ul>
  
    <p>
      We believe you have the skills and expertise required to excel in this
      role, and we are excited to have you on board.
    </p>
  
    <p>
      We welcome you to our Inache family as a CR. We look forward to working
      with you to make a difference in our community.
    </p>
  
    <p>
      Note - Please use your current email.id and Password to log into Inache.
    </p>
  
    <p>Best regards,</p>
  
    <p>Inache</p>
  </div>
  
""",
    'subject': "Welcome to Inache as CR of {factory_unit_number}",
    'title': "Second Onboarding Mail in case of Multiple Role as CR",
    'variables': {"user_name": "user_name","factory_unit_number":"factory_unit_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
} 
,{
    'body': """<div style="margin-top: 20px;">
    <p>Dear {user_name},</p>
  
    <p>
      We are pleased to inform you that you have been assigned a new role to you
      on Inache.
    </p>
  
    <p>
      As part of the CM of {factory_unit_number}, you will be responsible for:
    </p>
  
    <ul>
      <li>Assessing Case Report prepared by CR.</li>
      <li>Assigning the Case Report to the designated Case Troubleshooter.</li>
    </ul>
  
    <p>
      We believe you have the skills and expertise required to excel in this
      role, and we are excited to have you on board.
    </p>
  
    <p>
      We welcome you to our Inache family as a CM. We look forward to working
      with you to make a difference in our community.
    </p>
  
    <p>
      Note - Please use your current email.id and Password to log into Inache.
    </p>
  
    <p>Best regards,</p>
  
    <p>Inache</p>
  </div>  
""",
    'subject': "Welcome to Inache as CM of {factory_unit_number}",
    'title': "Second Onboarding Mail in case of Multiple Role as CM",
    'variables': {"user_name": "user_name", "factory_unit_number":"factory_unit_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
} 
,{
    'body': """<div style="margin-top: 20px;">
    <p>Dear {user_name},</p>
  
    <p>
      We are pleased to inform you that you have been assigned a new role to you
      on Inache.
    </p>
  
    <p>
      As part of the CT of {factory_unit_number}, you will be responsible for:
    </p>
  
    <ul>
      <li>Assessing Case Report filled by CR & CM.</li>
      <li>Seeking information from workers/complainants for better resolution.</li>
      <li>Resolving & Closing the case within the provided timeline.</li>
    </ul>
  
    <p>
      We believe you have the skills and expertise required to excel in this
      role, and we are excited to have you on board.
    </p>
  
    <p>
      We welcome you to our Inache family as a CT. We look forward to working
      with you to make a difference in our community.
    </p>
  
    <p>
      Note - Please use your current email.id and Password to log into Inache.
    </p>
  
    <p>Best regards,</p>
  
    <p>Inache</p>
  </div>
    
""",
    'subject': "Welcome to Inache as CT of {factory_unit_number}    ",
    'title': "Second Onboarding Mail in case of Multiple Role as CT",
    'variables': {"user_name": "user_name", "factory_unit_number":"factory_unit_number"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},

{
    'body': """<div style="margin-top: 20px;">
  <p>Dear {user_name},</p>
  <p>
    We are pleased to onboard you as a Regional Admin on Inache.
  </p>
  <p>
    To get started with your new role, follow the steps below:
  </p>
  <ol>
    <li>Click on the following link to create a new password {password_reset_link}</li>
    <li>Create a strong password.</li>
    <li>Confirm your new Password.</li>
  </ol>
  <p>
    Note: The password reset link will only be accessible for 2 days.
  </p>
  <p>
    As Regional Admin, you have the following responsibilities:
  </p>
  <ul>
    <li>Regional Admin will be authorized to create, edit, or delete factories.</li>
    <li>You can create, edit, or delete Users.</li>
    <li>Responsible for preparing case reports for POSH and Special Cases.</li>
  </ul>
  <p>
    We believe you have the skills and expertise required to excel in this
    role, and we are excited to have you on board.
  </p>
  <p>Best regards,</p>
  <p>Inache</p>
</div>
    
""",
    'subject': "Welcome to Inache as Regional Admin",
    'title': "Onboarding Mail for Regional Admin",
    'variables': {"user_name": "user_name", "password_reset_link":"password_reset_link"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
},
{
    'body': """<div style="margin-top: 20px;">
  <p>Dear {user_name},</p>
  <p>
    We are pleased to onboard you as a Super Admin on Inache.
  </p>
  <p>
    To get started with your new role, follow the steps below:
  </p>
  <ol>
    <li>Click on the following link to create a new password {password_reset_link}</li>
    <li>Create a strong password.</li>
    <li>Confirm your new Password.</li>
  </ol>
  <p>
    Note: The password reset link will only be accessible for 2 days.
  </p>
  <p>
    As Super Admin, you have the following responsibilities:
  </p>
  <ul>
    <li>Super Admin can create, edit, or delete a Region.</li>
    <li>Assign Regional Admin to Region.</li>
    <li>Create, edit, or delete factories.</li>
    <li>Create, edit, or delete Users.</li>
  </ul>
  <p>
    We believe you have the skills and expertise required to excel in this
    role, and we are excited to have you on board.
  </p>
  <p>Best regards,</p>
  <p>Inache</p>
</div>

    
""",
    'subject': "Welcome to Inache as Super Admin",
    'title': "Onboarding mail for Super Admin",
    'variables': {"user_name": "user_name", "password_reset_link":"password_reset_link"},
    'language': "English",
    'company_fk': 1,
    'template_category': "Email"
} 


,{
  'body': """<div style="margin-top: 20px;">
  <p>Dear {user_name},</p>

  <p>
    I trust this message finds you well. I'm writing to remind you about a case
   {case_number} that is awaiting closure due to a lack of response from the worker
    involved. It has been 72 hours since the last communication.
  </p>

  <p>
    Case ID: {case_number}<br />
    Status: Awaiting Worker Response
  </p>

  <p>
    As per our protocol, cases should be closed if there is no worker response
    within 72 hours. This helps us maintain efficient case management and
    ensures that issues are addressed promptly.
  </p>

  <p>
    Kindly review the case and determine if the worker has provided the
    required information. If not, please proceed with closing the case.
  </p>

  <p>Your adherence to our procedures is greatly appreciated.</p>

  <p>Thank you for your attention to this matter.</p>

  <p>Best regards, Inache</p>
</div>

""",
  'subject': "Reminder: Pending Case Closure for Lack of Worker Response",
  'title': "Worker hasn't replied within 72hrs - RA",
  'variables': {"user_name": "user_name", "case_number":"case_number"},
  'language': "English",
  'company_fk': 1,
  'template_category': "Email"
} ,{
  'body': """<div style="margin-top: 20px;">
  <p>Dear {user_name},</p>

  <p>
    I trust this message finds you well. I'm writing to remind you about a case
    {case_number} that is awaiting closure due to a lack of response from the worker
    involved. It has been 72 hours since the last communication.
  </p>

  <p>
    Case ID: {case_number}<br />
    Status: Awaiting Worker Response
  </p>

  <p>
    As per our protocol, cases should be closed if there is no worker response
    within 72 hours. This helps us maintain efficient case management and
    ensures that issues are addressed promptly.
  </p>

  <p>
    Kindly review the case and determine if the worker has provided the
    required information. If not, please proceed with closing the case.
  </p>

  <p>Your adherence to our procedures is greatly appreciated.</p>

  <p>Thank you for your attention to this matter.</p>

  <p>Best regards, Inache</p>
</div>

""",
  'subject': "Reminder: Pending Case Closure for Lack of Worker Response",
  'title': "Worker hasn't replied within 72hrs - CT",
  'variables': {"user_name": "user_name", "case_number":"case_number"},
  'language': "English",
  'company_fk': 1,
  'template_category': "Email"
} 
]

    for template in templates:
           SNSTemplate.objects.get_or_create(
              template_id = uuid.uuid4(),
              body=template['body'],
              subject=template['subject'],
              title=template['title'],
              variables=template['variables'],
              language=template['language'],
              company_fk=Company.objects.get(id=template['company_fk']),
              template_category=template['template_category']
          )   
    return Response("success",)
    