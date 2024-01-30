import csv
from email.mime.base import MIMEBase
from accounts.models import BaseUserModel, NotificationLog
from django.core.mail import EmailMessage
from email.mime.base import MIMEBase
from email import encoders

def cases_csv(data,email,notification,formatted_email,subject):
    with open('cases.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'Unit Number/ Factory Number',
            'Case Number',
            'Case Created on DateTime',
            'Case Reporter',
            'Case Manager',
            'Case TroubleShooter',
            'Case Assigned to CR DateTime',
            'Case Assigned to CM DateTime',
            'Case Assigned to CT DateTime',
            'First Response sent by CT Date Time',
            'Resolved Datetime',
            'Closed Datetime',
            'Category',
            'Sub Category',
            ]           
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        for row in data['case_csv']:
            writer.writerow(row)
    context={'account':{'user_name':BaseUserModel.objects.get(id=data['user_id']).user_name}}
    # html_message = render_to_string('accounts/coallate.html',context=context)
    logs = { "send_to" : email, "send_from" : "no-reply@inache.co" }

    NotificationLog.objects.create(notification_fk=notification,message_subject=subject,message_content=formatted_email,template_fk=notification.template_fk,sns_topic_name="Test Topic",notification_type="email", log=logs, event_identifier=event_identifier)

    emailbody = EmailMessage(subject, formatted_email, "no-reply@inache.co", [email])
    with open('cases.csv', "rb") as file:
        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", f"attachment; filename={'cases.csv'}")
        emailbody.attach(attachment)
    emailbody.send(fail_silently=False)