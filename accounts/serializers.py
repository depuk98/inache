import datetime
import json
import os
import random
from calendar import SATURDAY
from datetime import timedelta
import boto3
import pytz
import os
import math
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.timezone import localtime
from InacheBackend.settings.base import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SES_REGION_NAME
from accounts.classes.AwsUtil import AwsUtil
from accounts.validators import CSVFileValidator
# from accounts.celery_tasks import send_user_email
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import send_mail as sm
from accounts.stringUtils import reopen_number
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import exceptions
from accounts.utils import current_time
import accounts
from accounts.models import (
    AuditLog,
    SMSTemplates,
    BaseUserModel,
    Case,
    CaseReslovingReport,
    Company,
    Factory,
    ReopenCase,
    AwarenessProgram,
    FactoryDepartment,
    Complainer,
    BroadcastMessage,
    ProgramAttachment,
    HolidayCalendar,
    UserRoleFactory,
    Incentives,
    FactoryRegion,
    SNSTemplate
)
from accounts.Utils.userRoleParser import parser
from accounts.utils import Util
from accounts.dateUtils import working_days, count_working_hours
from accounts.constants import ActionTypes, UserRole, CaseStatus, UserResposibilities, CaseActiveStatus

class UserRoleFactorySerializerAll(serializers.ModelSerializer):
    class Meta:
        model=UserRoleFactory
        fields="__all__"
    
class CsvSerializer(serializers.Serializer):
    csv_file = serializers.FileField(validators=[CSVFileValidator()])

class CompanySerializer(serializers.ModelSerializer): #serializer for company
    class Meta:
        model = Company
        fields = "__all__"
class BaseUserModelSerializer(serializers.ModelSerializer): #serializer fur baseusermodel
   
    class Meta:
        model = BaseUserModel
        exclude = [ 'created_at','last_login','is_superuser','is_staff','is_active','password',]

class CaseRepQCSerializer(serializers.ModelSerializer): #serializes case reps so they can be sent to frontend to be assigned as qc for a factory
    
    class Meta:
        model = BaseUserModel
        exclude = [ 'created_at', 'updated_at', 'deleted_at','mobile_number','password','groups','user_permissions','is_superuser','is_staff','is_active','last_login',]
class CaseManQCSerializer(serializers.ModelSerializer): #serializes case mans so they can be sent to frontend to be assigned as qc for a factory
    
    class Meta:
        model = BaseUserModel
        exclude = [ 'created_at', 'updated_at', 'deleted_at','mobile_number','password','groups','user_permissions','is_superuser','is_staff','is_active','last_login',]
class CaseTrbQCSerializer(serializers.ModelSerializer): #serializes case trbs so they can be sent to frontend to be assigned as qc for a factory
    
    class Meta:
        model = BaseUserModel
        exclude = [ 'created_at', 'updated_at', 'deleted_at','mobile_number','password','groups','user_permissions','is_superuser','is_staff','is_active','last_login',]



class FactorySerializer(serializers.ModelSerializer): #serializer for factory models
    class Meta:
        model = Factory
        fields = "__all__"

class FactoryDepartmentSerializer(serializers.ModelSerializer):  # serializer for factory models
    class Meta:
        model = FactoryDepartment
        fields = "__all__"

class ComplainerSerializer(serializers.ModelSerializer):  # serializer for factory models
    class Meta:
        model = Complainer
        fields = "__all__"





class CompanyFactoryPostSerializer(serializers.ModelSerializer): #serializer for adding a factory for a company
    class Meta:
        model = Factory
        exclude = ['Company']
        # fields="__all__"
class CaseRequestSerializerCR(serializers.Serializer): 
    #CaseDetails=serializers.CharField(required=True)
    CaseValidation=serializers.BooleanField(required=True)
    CaseNature=serializers.CharField(required=True)
    #SubCategory=serializers.CharField(required=True)
    #CaseCategory=serializers.CharField(required=True)
    #Priority=serializers.CharField(required=True)
    #CommentsByRep= serializers.CharField(required=True)
    #CaseManager=serializers.IntegerField(required=True)
class CaseRequestSerializerCM(serializers.Serializer): 
    CaseValidation=serializers.BooleanField(required=True)
    CaseNature=serializers.CharField(required=True)
    SubCategory=serializers.CharField(required=True)
    CaseCategory=serializers.CharField(required=True)
    Priority=serializers.CharField(required=True)
    CommentsByMan= serializers.CharField(required=True)
    CaseTroubleShooter=serializers.IntegerField(required=True)

class CaseSerializers(serializers.ModelSerializer): #serializer for case
    class Meta:
        model=Case
        fields="__all__"
class UserPermissionsSerializer(serializers.Serializer):
    hasAccess_BroadCast_Message = serializers.BooleanField(required=True)
    hasAccess_Holiday_Calender = serializers.BooleanField(required=True)
    hasAccess_Awareness_Program = serializers.BooleanField(required=True)
class UserPostRequestSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    role = serializers.CharField(required=True)
    company_fk = serializers.IntegerField(required=True)
    user_permissions = serializers.DictField(required=True)
    gender = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    mobile_number = serializers.CharField(required=True)
class UserRolePostRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    role = serializers.CharField(required=True)
    company_fk = serializers.IntegerField(required=True)
    user_permissions = serializers.DictField(required=True)
class ProgramAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramAttachment
        fields = '__all__'

class UserRoleFactorySerializer(serializers.ModelSerializer):
    class Meta:
        model=UserRoleFactory
        # fields="__all__"
        exclude =['role', 'user_permissions']

class AwarenessProgramSerializer(serializers.ModelSerializer): 
    Attachements = serializers.ListField(child=serializers.FileField(), required=False, write_only=True)
    attachments = ProgramAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = AwarenessProgram
        fields = "__all__"
        extra_fields = ['attachments']
    
    def create(self, validated_data):
        files_data = validated_data.pop('Attachements', [])
        validated_data.pop('Files', [])
        print(validated_data, files_data)

        program = AwarenessProgram.objects.create(**validated_data)
        for file_data in files_data:
            attachment = ProgramAttachment.objects.create(Attachement=file_data, awarenessProgram=program)
        return program

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime

class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        hash_value =(
            str(user.pk)  +
            str(user.password) +
            str(timestamp + timedelta(days=5).total_seconds())
        )
        return hash_value
class SNSTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNSTemplate
        fields = "__all__"


class createuserserializer(serializers.ModelSerializer): #serializer for registering user 
    # password2 = serializers.CharField(
    #     style={"input_type": "password"}, write_only=True)
        
    class Meta:
        model = BaseUserModel
        fields = ['user_name','email','company_fk','name','gender','mobile_number']
        # exclude = ['uuid','created_at','updated_at','deleted_at','is_staff' ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = "vouge2023/"
        if BaseUserModel.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'Email Already Exists'})
        # name=self.validated_data['username']
        print(self.validated_data)
        user = self.context['request'].user
        # if(self.validated_data['role']=="SUPER_ADMIN" or self.validated_data['role']=="FACTORY_ADMIN" or self.validated_data['role']=="INACHE_ADMIN"):
        account = BaseUserModel(
            email=self.validated_data['email'], user_name=self.validated_data['user_name'],company_fk=self.validated_data["company_fk"],\
                name=self.validated_data['name'],gender=self.validated_data['gender'],mobile_number=str(self.validated_data['mobile_number']))
            
        if user=="AnonymousUser":
            account.created_by="AdminUser"
        else:
            account.created_by=user
        account.set_password(password)
        account.save()
        custom_token_generator = CustomTokenGenerator()

        uidb64 = urlsafe_base64_encode(smart_bytes(account.id))
        token = custom_token_generator.make_token(account)
        # token=PasswordResetTokenGenerator().make_token(user)
        # current_site=get_current_site(request=self.context['request'])
        # relative_link=reverse('password_reset_confirm', kwargs={'uidb64':uidb64,'token':token})
        
        if os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.dev':
                link = 'http://localhost:3000/resetPassword/?'
        elif os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.staging':
            link = 'https://staging.inache.co/resetPassword/?'
        elif os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.production':
            link = 'https://inache.co/resetPassword/?'
        absurl = link + \
                'uidb64=' + str(uidb64) + '&token='+str(token) 
        # absurl = 'http://localhost:3000/resetPassword/?' + \
        #     'uidb64=' + str(uidb64) + '&token='+str(token) 
        Responsibilities = UserResposibilities.FACTORY_ADMIN if self.context['request'].data['role']=="FACTORY_ADMIN" else UserResposibilities.CR if self.context['request'].data['role']=="CR" else UserResposibilities.CM if self.context['request'].data['role']=="CM" else UserResposibilities.CT if self.context['request'].data['role']=="CT" else UserResposibilities.FACTORY_ADMIN
        Responsibilities=Responsibilities.split("-")
        context={
            'account': {
            'user_name': account.user_name,
            'email':account.email,
            'role': self.context['request'].data['role'],
            'password':password,
            'Responsibilities':Responsibilities,
            'absurl':absurl

        },
        'org_name': account.company_fk.Legalcompanyname
        }
        html_message = render_to_string('accounts/onboarding.html',context=context)
        # print(html_hismessage)
        # send_mail(account.email,html_message,)
        # res=sm(
        # subject='Welcome!!',
        # message='',
        # html_message=html_message,
        # from_email='no-reply@inache.co',
        # recipient_list=[account.email],
        # fail_silently=False,
        #     )
        # sns_client = boto3.client('sns', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_SES_REGION_NAME)

        message_data = {
            'eventType': 'userNotification',
            'emailList': [account.email],
            'subject': 'Welcome!!!',
            'message': html_message,
        }
        TopicArn='arn:aws:sns:ap-south-1:300380748892:Test_Topic'

        print(html_message)
        aws= AwsUtil(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SES_REGION_NAME)
        response=aws.publish_message_to_sns(TopicArn,message_data)
        # Publish the message to the SNS topic with MessageAttributes
        # response = sns_client.publish(
        #     Message=json.dumps({'default': json.dumps(message_data)}),
        #     MessageStructure='json',
        #     MessageAttributes={
        #         'event_type': {
        #             'DataType': 'String',
        #             'StringValue': 'userNotification',
        #         },
        #     },
        # )
    # Optionally, you can log or handle the response from SNS
        # print(f'Message sent to SNS topic with message ID: {response["MessageId"]}')
        # Util.send_email(data)
        
        # send the email
        return account

class CaseUploadSerializer(serializers.ModelSerializer): #serializer to upload an inperson casetto
    class Meta:
        model=Case
        fields="__all__"
        
    def save(self):
        # n = random.randint(0,10000)
       
        case=Case(Factory=self.validated_data['Factory'],Company=self.validated_data['Company'],ReportingMedium=self.validated_data['ReportingMedium'],CaseStatus=self.validated_data['CaseStatus'],CommentsByRep=self.validated_data['CommentsByRep'],MessagebyWorker=self.validated_data['MessagebyWorker'],workerLanguage=self.validated_data['workerLanguage'])
            
        case.save()
        return case


class CaseFileUploadSerializer(serializers.ModelSerializer): #serializer to upload suggestion box and worker commitie cases
    class Meta:
        model = Case
        fields="__all__"
    # def save(self):
        

class QCReviewSerializer(serializers.ModelSerializer): #serializer for qc to review a case
    class Meta:
        model=Case
        fields=["Counter"]

class CaseResolvingReportAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model=CaseReslovingReport
        fields="__all__"

    def save(self):
        case=CaseReslovingReport(Case=self.validated_data['Case'],CCRWhen=self.validated_data['CCRWhen'],CCRWhere=self.validated_data['CCRWhere'],CCRWhathappened=self.validated_data['CCRWhathappened'],CCRWho=self.validated_data['CCRWho'],CCRremarks=self.validated_data['CCRremarks'],CCMessage=self.validated_data['CCMessage'],CCTemplate=self.validated_data['CCTemplate'],CCLanguage=self.validated_data['CCLanguage'],CCRvariables=self.validated_data['CCRvariables'],CCRComments_RA=self.validated_data['CCRComments_RA'])
        ss=self.validated_data['Case']
        case1=Case.objects.get(pk=ss.id)
        template = SMSTemplates.objects.get(Title=self.validated_data['CCTemplate'],language=self.validated_data['CCLanguage'],Company=case1.Company)
        if ("Unresponsive Message" in template.template_categories) or ("Posh Unresponsive Message" in template.template_categories):
            case1.CaseStatus = CaseStatus.UNRESPONSIVE
            case1.ClosingTime = current_time()
            case1.CurrentStatus = CaseActiveStatus.NEW_CASE
            newstate=case1.save()
            case.save()
            # print(self.context.get("Message"))
            
            auditlog = AuditLog.objects.create(
                case=case1,
                status=case1.CaseStatus,
                created_by=case1.RegionalAdmin,
                prev_state=str(case1),
                current_state=str(newstate),
                action_type=ActionTypes.CASE_UNRESPONSIVE,
            )
        elif ("Posh Message" in template.template_categories):
            case1.CaseStatus = CaseStatus.CLOSED
            case1.ClosingTime = current_time()
            case1.CurrentStatus = CaseActiveStatus.NEW_CASE
            newstate=case1.save()
            case.save()
            # print(self.context.get("Message"))
            
            auditlog = AuditLog.objects.create(
                case=case1,
                status=case1.CaseStatus,
                created_by=case1.RegionalAdmin,
                prev_state=str(case1),
                current_state=str(newstate),
                action_type=ActionTypes.CASE_CLOSED,
            )
            
        else:
            case1.CaseStatus = CaseStatus.RESOLVED
            case1.ResolveTime=current_time()
            case1.CurrentStatus = CaseActiveStatus.NEW_CASE
            newstate=case1.save()
            case.save()
            # print(self.context.get("Message"))
            
            auditlog = AuditLog.objects.create(
                case=case1,
                status=case1.CaseStatus,
                created_by=case1.RegionalAdmin,
                prev_state=str(case1),
                current_state=str(newstate),
                action_type=ActionTypes.CASE_RESOLVED_RA,
            )
        return case


class CaseResolvingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model=CaseReslovingReport
        fields="__all__"

class CaseReportSerializers(serializers.ModelSerializer):
    class Meta:
        model=CaseReslovingReport
        fields = "__all__"

    def save(self):
        # dictionary containing all the subcategories with their predefined priority
        pricat = {"Canteen food":"Medium", "Canteen cleanliness & infrastructure":"Minor", "Factory temperature & conditions":"Medium", "Machine maintenance":"Medium", "PPE":"Minor",
            "Shop Floor cleanliness":"Minor", "Washroom cleanliness":"Minor", "Leave":"Medium", "Absenteeism":"Medium",
            "Conflict with People Officer":["Major","Level 1"], "Conflict with co-worker":["Major","Level 1"], "Welfare schemes":"Medium", "Other facilities":"Minor", "Transport":"Minor","Dormitory":"Minor",
            "PF":"Medium", "ESI":"Medium", "Full and final":"Medium", "Compensation & Benefits":"Medium", "Sexual harassment":"Major", "Case against influential managers":["Major","Level 1"],
            "Dispensary facilities":"Medium","Others":"Minor"}
        case=CaseReslovingReport(Case=self.validated_data['Case'],CCRWhen=self.validated_data['CCRWhen'],CCRWhere=self.validated_data['CCRWhere'],CCRWhathappened=self.validated_data['CCRWhathappened'],CCRWho=self.validated_data['CCRWho'],CCRremarks=self.validated_data['CCRremarks'],CCMessage=self.validated_data['CCMessage'],CCTemplate=self.validated_data['CCTemplate'],CCLanguage=self.validated_data['CCLanguage'],CCRvariables=self.validated_data['CCRvariables'])
        ss=self.validated_data['Case']
        case1=Case.objects.get(pk=ss.id)
        case1.Counter=5
        case1.CaseStatus = CaseStatus.RESOLVED
        case1.CurrentStatus = CaseActiveStatus.NEW_CASE
        T3vrfDate = localtime(case1.T3vrfDate)
        T2vrfDate = localtime(case1.T2vrfDate)
        case1.ResolveTime=current_time()
        caseFreeze = Incentives.objects.get(Case=case1)
        #if phone number exists, T2 exists and T3 starts from the time message sent
        if case1.T2Breached==True or case1.T2Breached==False:
            startDate = T3vrfDate
        #if no phone number, no send message, so no T2, so T3 starts from the time ct gets the case
        elif case1.T2Breached==None:
            startDate = T2vrfDate
        endDate = case1.ResolveTime
        sub=case1.SubCategory #subcategory given by cr
        # if caseFreeze.valid == False:
        #     case1.T3Breached = False
        # elif (caseFreeze.CTsendDate is not None) and (caseFreeze.CTreceiveDate is None):
        #     caseFreeze.valid = False
        #     case1.T3Breached = False
        # else:
        if caseFreeze.CTreceiveDate:
            working_hours = count_working_hours(startDate,caseFreeze.CTsendDate,case1.Factory) + count_working_hours(caseFreeze.CTreceiveDate,endDate,case1.Factory)
            days = math.ceil(working_hours/24)
        else:
            days = working_days(startDate,endDate,case1.Factory)
        if pricat[sub]=="Minor":
            #if the subcategory is minor or medium, sla depends on whether cr selects internal or external
            if case1.Priority == "Minor Grievance (Internal)":
                sla = 3 # if cr selects internal
                if days <= sla:
                    case1.T3 = 1
                    case1.t3c1 = False
                    case1.T3Breached = False
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c2 = None
                else:
                    case1.T3 = days
                    case1.T3Breached = True
                    case1.t3c1 = True
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c2 = None
            else:  #if cr selected external
                sla =30
                if days <= sla:
                    case1.T3 = 1
                    case1.t3c2 = False
                    case1.T3Breached = False
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c1 = None
                else:
                    case1.T3 = days
                    case1.T3Breached = True
                    case1.t3c2 = True
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c1 = None
        elif pricat[sub] == "Medium":
            if case1.Priority == "Medium Grievance (Internal)":
                sla =3
                if days <= sla:
                    case1.T3 = 1
                    case1.t3b1 = False
                    case1.T3Breached = False
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b2 = None
                    case1.t3c1 = None
                    case1.t3c2 = None
                else:
                    case1.T3 = days
                    case1.T3Breached = True
                    case1.t3b1 = True
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b2 = None
                    case1.t3c1 = None
                    case1.t3c2 = None
            else:
                sla =7
                if days <= sla:
                    case1.T3 = 1
                    case1.t3b2 = False
                    case1.T3Breached = False
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3c1 = None
                    case1.t3c2 = None
                else:
                    case1.T3 = days
                    case1.T3Breached = True
                    case1.t3b2 = True
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3c1 = None
                    case1.t3c2 = None
        # for a subcategory in major, the levels are also predefined, so no input needed from cr
        elif pricat[sub][0] == "Major":
            if pricat[sub][1] == "Level 1":
                sla =7
                if days <= sla:
                    case1.T3 = 1
                    case1.t3a1 = False
                    case1.T3Breached = False
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c1 = None
                    case1.t3c2 = None
                else:
                    case1.T3 = days
                    case1.T3Breached = True
                    case1.t3a1 = True
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c1 = None
                    case1.t3c2 = None
            else:
                sla =3
                if days <= sla:
                    case1.T3 = 1
                    case1.t3a2 = False
                    case1.T3Breached = False
                    case1.t3a1 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c1 = None
                    case1.t3c2 = None
                else:
                    case1.T3 = days
                    case1.T3Breached = True
                    case1.t3a2 = True
                    case1.t3a1 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c1 = None
                    case1.t3c2 = None
        else:
            sla=90
            if days <= sla:
                case1.T3 = 1
                case1.T3Breached = False
                case1.t3a1 = None
                case1.t3a2 = None
                case1.t3b1= None
                case1.t3b2 = None
                case1.t3c1 = None
                case1.t3c2 = None
            else:
                case1.T3 = days
                case1.T3Breached = True
                case1.t3a1 = None
                case1.t3a2 = None
                case1.t3b1= None
                case1.t3b2 = None
                case1.t3c1 = None
                case1.t3c2 = None
        if case1.Breached != True:
            if (case1.T0Breached==False and case1.T1Breached==False and case1.T2Breached!=True and case1.T3Breached==False):
                case1.Breached = False
            else:
                case1.Breached = True
        newstate=case1.save()
        case.save()
        # print(self.context.get("Message"))
        
        auditlog = AuditLog.objects.create(
            case=case1,
            status=CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,
            created_by=case1.CaseTroubleShooter,
            prev_state=str(case1),
            current_state=str(newstate),
            action_type=ActionTypes.CASE_RESOLVED_CT,
        )
        return case



class CaseResolvingReportUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model=CaseReslovingReport
        fields="__all__"
        
    def save(self):
        n = random.randint(0,10000)
        # dictionary containing all the subcategories with their predefined priority
        pricat = {"Canteen food":"Medium", "Canteen cleanliness & infrastructure":"Minor", "Factory temperature & conditions":"Medium", "Machine maintenance":"Medium", "PPE":"Minor",
            "Shop Floor cleanliness":"Minor", "Washroom cleanliness":"Minor", "Leave":"Medium", "Absenteeism":"Medium",
            "Conflict with People Officer":["Major","Level 1"], "Conflict with co-worker":["Major","Level 1"], "Welfare schemes":"Medium", "Other facilities":"Minor", "Transport":"Minor","Dormitory":"Minor",
            "PF":"Medium", "ESI":"Medium", "Full and final":"Medium", "Compensation & Benefits":"Medium", "Sexual harassment":"Major", "Case against influential managers":["Major","Level 1"],
            "Dispensary facilities":"Medium","Others":"Minor"}
        case=CaseReslovingReport(Case=self.validated_data['Case'],CCRWhen=self.validated_data['CCRWhen'],CCRWhere=self.validated_data['CCRWhere'],CCRWhathappened=self.validated_data['CCRWhathappened'],CCRWho=self.validated_data['CCRWho'],CCRremarks=self.validated_data['CCRremarks'],CCMessage=self.validated_data['CCMessage'],CCTemplate=self.validated_data['CCTemplate'],CCLanguage=self.validated_data['CCLanguage'],CCRvariables=self.validated_data['CCRvariables'])
        ss=self.validated_data['Case']
        case1=Case.objects.get(pk=ss.id)
        case1.Counter=5
        case1.CaseStatus = CaseStatus.RESOLVED
        case1.CurrentStatus = CaseActiveStatus.NEW_CASE
        T3vrfDate = localtime(case1.T3vrfDate)
        T2vrfDate = localtime(case1.T2vrfDate)
        case1.ResolveTime=current_time()
        caseFreeze = Incentives.objects.get(Case=case1)
        #if phone number exists, T2 exists and T3 starts from the time message sent
        if case1.T2Breached==True or case1.T2Breached==False:
            startDate = T3vrfDate
        #if no phone number, no send message, so no T2, so T3 starts from the time ct gets the case
        elif case1.T2Breached==None:
            startDate = T2vrfDate
        endDate = case1.ResolveTime
        sub=case1.SubCategory #subcategory given by cr
        # if caseFreeze.valid == False:
        #     case1.T3Breached = False
        # elif (caseFreeze.CTsendDate is not None) and (caseFreeze.CTreceiveDate is None):
        #     caseFreeze.valid = False
        #     case1.T3Breached = False
        # else:
        if caseFreeze.CTreceiveDate:
            working_hours = count_working_hours(startDate,caseFreeze.CTsendDate,case1.Factory) + count_working_hours(caseFreeze.CTreceiveDate,endDate,case1.Factory)
            days = math.ceil(working_hours/24)
        else:
            days = working_days(startDate,endDate,case1.Factory)
        if pricat[sub]=="Minor":
            #if the subcategory is medium, sla depends on whether cr selects internal or external
            if case1.Priority == "Minor Grievance (Internal)":
                sla = 3 # if cr selects internal
                if days <= sla:
                    case1.T3 = 1
                    case1.t3c1 = False
                    case1.T3Breached = False
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c2 = None
                else:
                    case1.T3 = days
                    case1.T3Breached = True
                    case1.t3c1 = True
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c2 = None
            else:  #if cr selected external
                sla =30
                if days <= sla:
                    case1.T3 = 1
                    case1.t3c2 = False
                    case1.T3Breached = False
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c1 = None
                else:
                    case1.T3 = days
                    case1.T3Breached = True
                    case1.t3c2 = True
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c1 = None
        elif pricat[sub] == "Medium":
            if case1.Priority == "Medium Grievance (Internal)":
                sla =3
                if days <= sla:
                    case1.T3 = 1
                    case1.t3b1 = False
                    case1.T3Breached = False
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b2 = None
                    case1.t3c1 = None
                    case1.t3c2 = None
                else:
                    case1.T3 = days
                    case1.T3Breached = True
                    case1.t3b1 = True
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b2 = None
                    case1.t3c1 = None
                    case1.t3c2 = None
            else:
                sla =7
                if days <= sla:
                    case1.T3 = 1
                    case1.t3b2 = False
                    case1.T3Breached = False
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3c1 = None
                    case1.t3c2 = None
                else:
                    case1.T3 = days
                    case1.T3Breached = True
                    case1.t3b2 = True
                    case1.t3a1 = None
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3c1 = None
                    case1.t3c2 = None
        # for a subcategory in major, the levels are also predefined, so no input needed from cr
        elif pricat[sub][0] == "Major":
            if pricat[sub][1] == "Level 1":
                sla =7
                if days <= sla:
                    case1.T3 = 1
                    case1.t3a1 = False
                    case1.T3Breached = False
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c1 = None
                    case1.t3c2 = None
                else:
                    case1.T3 = days
                    case1.T3Breached = True
                    case1.t3a1 = True
                    case1.t3a2 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c1 = None
                    case1.t3c2 = None
            else:
                sla =3
                if days <= sla:
                    case1.T3 = 1
                    case1.t3a2 = False
                    case1.T3Breached = False
                    case1.t3a1 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c1 = None
                    case1.t3c2 = None
                else:
                    case1.T3 = days
                    case1.T3Breached = True
                    case1.t3a2 = True
                    case1.t3a1 = None
                    case1.t3b1= None
                    case1.t3b2 = None
                    case1.t3c1 = None
                    case1.t3c2 = None
        else:
            sla=90
            if days <= sla:
                case1.T3 = 1
                case1.T3Breached = False
                case1.t3a1 = None
                case1.t3a2 = None
                case1.t3b1= None
                case1.t3b2 = None
                case1.t3c1 = None
                case1.t3c2 = None
            else:
                case1.T3 = days
                case1.T3Breached = True
                case1.t3a1 = None
                case1.t3a2 = None
                case1.t3b1= None
                case1.t3b2 = None
                case1.t3c1 = None
                case1.t3c2 = None
        if case1.Breached != True:
            if (case1.T0Breached==False and case1.T1Breached==False and case1.T2Breached!=True and case1.T3Breached==False):
                case1.Breached = False
            else:
                case1.Breached = True
        newstate=case1.save()
        case.save()
        # print(self.context.get("Message"))
       
        auditlog = AuditLog.objects.create(
            case=case1,
            status=CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,
            created_by=case1.CaseTroubleShooter,
            prev_state=str(case1),
            current_state=str(newstate),
            action_type=ActionTypes.CASE_RESOLVED_CT,
        )

        return case
class QCCaseReopenSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReopenCase
        fields="__all__"
        
    def save(self):
        n = random.randint(0,10000)

        reopencase=ReopenCase(Case=self.validated_data['Case'],TOC=self.validated_data['TOC'],IC=self.validated_data['IC'],QOE=self.validated_data['QOE'],Remarks=self.validated_data['Remarks'])
        ss=self.validated_data['Case']
        # print(ss.id)
        case1=Case.objects.get(pk=ss.id)
        num=case1.CaseNumber
        num = reopen_number(num)

        case=Case.objects.create(CaseNumber=num,Company=case1.Company,Factory=case1.Factory,Counter=1,CaseStatus=CaseStatus.ASSIGNED_TO_REPORTER, T1vrfDate=current_time())
        if accounts.views.assigncR(num)==False:
            pass
        reopencase.save()
        return reopencase
class CaseReopenSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReopenCase
        fields="__all__"
        
    def save(self):
        userRole=parser(self.context['request'])
        if userRole is None:
            raise exceptions.PermissionDenied({"error":"ROLE ID NOT PRESENT"})
        if userRole.role.role==UserRole.CASE_TROUBLESHOOTER:
            reopencase=ReopenCase(Case=self.validated_data['Case'],Remarks="Reopened By CT")
        elif userRole.role.role==UserRole.REGIONAL_ADMIN:
            reopencase=ReopenCase(Case=self.validated_data['Case'],Remarks="Reopened By RA")
        svd=self.validated_data['Case']
        # print(type(ss))
        case1=Case.objects.get(pk=svd.id)
        num=case1.CaseNumber
        num = reopen_number(num)
        case=Case.objects.create(CaseNumber=num,Company=case1.Company,Factory=case1.Factory,Counter=1,CaseStatus=CaseStatus.ASSIGNED_TO_REPORTER,reopened=True, T1vrfDate=current_time())
        case1.CaseStatus=CaseStatus.CLOSED
        if accounts.views.assigncR(num)==False:
            pass
        case1.save()
        reopencase.save()
        return reopencase
class BroadcastMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BroadcastMessage
        fields = "__all__"

class PasswordResetLinkGenerator:
    @staticmethod
    def generate(user):
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        # token=PasswordResetTokenGenerator().make_token(user)
        custom_token_generator = CustomTokenGenerator()
        token = custom_token_generator.make_token(user)

        # current_site = get_current_site(request=request)
        # relative_link = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        
        # Define the base URL based on the environment
        base_url = {
            'InacheBackend.settings.dev': 'http://localhost:3000/resetPassword/?',
            'InacheBackend.settings.staging': 'https://staging.inache.co/resetPassword/?',
            'InacheBackend.settings.production': 'https://inache.co/resetPassword/?'
        }.get(os.environ.get('DJANGO_SETTINGS_MODULE'), 'http://localhost:3000/resetPassword/?')

        absurl = base_url + 'uidb64=' + str(uidb64) + '&token=' + str(token)
        return absurl
class ResetPasswordEmailSerializer(serializers.Serializer):
    # email=serializers.EmailField(min_length=2)
    # class Meta:
    #     fields=['email']
        
    # def validate(self, attrs):
    #     email = attrs.get('email','')
    #     if BaseUserModel.objects.filter(email=email).exists():
    #         user = BaseUserModel.objects.get(email=email)
    #         uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
    #         # token=PasswordResetTokenGenerator().make_token(user)
    #         custom_token_generator = CustomTokenGenerator()
    #         token = custom_token_generator.make_token(user)

    #         current_site=get_current_site(request=self.context['request'])
    #         relative_link=reverse('password_reset_confirm', kwargs={'uidb64':uidb64,'token':token})
    #         if os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.dev':
    #             link = 'http://localhost:3000/resetPassword/?'
    #         elif os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.staging':
    #             link = 'https://staging.inache.co/resetPassword/?'
    #         elif os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.production':
    #             link = 'https://inache.co/resetPassword/?'
    #         absurl = link + \
    #             'uidb64=' + str(uidb64) + '&token='+str(token)            
    #         email_body = 'Hello, \n Use link below to reset your password  \n' + \
    #         absurl
    #         res=sm(
    #         subject='Reset your passsword',
    #         message='',
    #         html_message=email_body,
    #         from_email='no-reply@inache.co',
    #         recipient_list=[user.email],
    #         fail_silently=False,
    #         )
    #         # data = {'email_body': email_body, 'to_email': user.email,
    #         #     'email_subject': 'Reset your passsword'}
    #         # Util.send_email(data)
    #     return super().validate(attrs)
        email = serializers.EmailField(min_length=2)
        class Meta:
            fields = ['email']
            
        def validate(self, attrs):
            email = attrs.get('email', '')
            if BaseUserModel.objects.filter(email=email).exists():
                user = BaseUserModel.objects.get(email=email)
                absurl = PasswordResetLinkGenerator.generate(user)

                email_body = 'Hello, \n Use link below to reset your password  \n' + absurl
                res = sm(
                    subject='Reset your passsword',
                    message='',
                    html_message=email_body,
                    from_email='no-reply@inache.co',
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                # data = {'email_body': email_body, 'to_email': user.email,
                #     'email_subject': 'Reset your passsword'}
                # Util.send_email(data)
            return super().validate(attrs)

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6,max_length=60,write_only=True)
    uidb64 = serializers.CharField(min_length=1,write_only=True)
    token = serializers.CharField(min_length=1,write_only=True)
    class Meta:
        fields=['password','uidb64','token']
    
    def validate(self,attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = BaseUserModel.objects.get(id=id)
            if not CustomTokenGenerator().check_token(user, token):
                raise AuthenticationFailed({'errorMessage': 'The reset link is invalid, Please ask your SUPER ADMIN to send another email'}, 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            print(e)
            raise AuthenticationFailed({'errorMessage': 'The reset link is invalid, Please ask your SUPER ADMIN to send another email'}, 401)
        return super().validate(attrs)
    
class SMSTemplatesSerializer(serializers.ModelSerializer):
    class Meta:

        model = SMSTemplates
        fields = "__all__"

class TemplateSerializer(serializers.Serializer):
    templateID = serializers.CharField(required=False)
    body = serializers.CharField(required=False)
    Title = serializers.CharField(required=False)
    language = serializers.CharField(required=False)
    Company = serializers.IntegerField(required=False)
    variables = serializers.JSONField(required=False)
    template_categories = serializers.JSONField(required=False)
    user_roles_access = serializers.JSONField(required=False)

    def update(self, instance, validated_data):
        instance.templateID = validated_data.get('templateID', instance.templateID)
        instance.body = validated_data.get('body', instance.body)
        instance.Title = validated_data.get('Title', instance.Title)
        instance.language = validated_data.get('language', instance.language)
        instance.Company = validated_data.get('Company', instance.Company)
        instance.variables = validated_data.get('variables', instance.variables)
        instance.template_categories = validated_data.get('template_categories', instance.template_categories)
        instance.user_roles_access = validated_data.get('user_roles_access', instance.user_roles_access)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

class setLanguagePreferenceSerializer(serializers.Serializer):
    Languages = serializers.JSONField(required=True)

class HolidayCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidayCalendar
        fields = '__all__'

class FactoryRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactoryRegion
        fields = '__all__'

class StartInputSerializer(serializers.Serializer):
        file_name = serializers.CharField()
        file_type = serializers.CharField()
        model = serializers.ChoiceField( choices=["awareness_program", "case", "profile_picture"])
        company_fk = serializers.IntegerField()
        id = serializers.CharField()

        def validate(self, attrs):
            validated_data = super().validate(attrs)
            request = self.context.get('request')

            model = validated_data.get('model')
            id = validated_data.get('id')
            try:
                Company.objects.get(id=validated_data.get('company_fk'))
            except Company.DoesNotExist:
                raise serializers.ValidationError("Invalid Company ID Provided")
            if model == 'awareness_program':
                
                if not AwarenessProgram.objects.filter(id=id).exists():
                    raise serializers.ValidationError("Invalid Awareness Program ID Provided")
                if request.user.company_fk.id!=AwarenessProgram.objects.get(id=id).Factory.Company.id or request.user.company_fk.id!=validated_data.get('company_fk'):
                    raise serializers.ValidationError("Company of user and to be uploaded program document are not same")
            if model == 'case': 
                if not Case.objects.filter(id=id).exists():
                    raise serializers.ValidationError("Invalid Case Number provided")
                if request.user.company_fk.id!=Case.objects.get(id=id).Company.id or request.user.company_fk.id!=validated_data.get('company_fk'):
                    raise serializers.ValidationError("Company of user and to be uploaded case document are not same")
            if model == 'profile_picture':
                if not BaseUserModel.objects.filter(id=id).exists():
                    raise serializers.ValidationError("Invalid User ID")
                if request.user.company_fk.id!=BaseUserModel.objects.get(id=id).company_fk.id or request.user.company_fk.id!=validated_data.get('company_fk'):
                    raise serializers.ValidationError("Company of user and to be uploaded profile picture are not same")     
            return validated_data
class FinishInputSerializer(serializers.Serializer):
        file_id = serializers.IntegerField()
        model_id = serializers.IntegerField()
        model=serializers.CharField()

class GetInputSerializer(serializers.Serializer):
        file_ids = serializers.CharField()