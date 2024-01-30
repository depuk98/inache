from __future__ import division
from email import encoders
from botocore.exceptions import ClientError
from django.core.mail import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ
from sqlite3 import register_converter
import traceback
from unittest import case
# from django.conf import settings
from django.shortcuts import get_object_or_404
import jwt
import requests
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
import csv
import datetime
import json
import random
from calendar import SATURDAY
from datetime import date, timedelta
from os import environ
from django.contrib.auth.models import Group, Permission
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import PermissionRequiredMixin
from InacheBackend import settings
from InacheBackend.settings.base import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SES_REGION_NAME
import accounts
from accounts.Service.SendMSGPermission import send_message_user_validation
from rest_framework.exceptions import AuthenticationFailed
from datetime import date
from accounts.Utils.userRoleParser import parser
from rest_framework.request import Request
import re
from functools import reduce
import urllib.request
from accounts.classes.AwsUtil import AwsUtil
from pydub import AudioSegment
import ssl
import subprocess
from pydub.utils import mediainfo
from pydub.silence import detect_silence
import speech_recognition as sr
from speech_recognition import UnknownValueError
import pytz
import requests
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db.models import Q, F
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
from accounts.Service.UploadService import FileDirectUploadService
from accounts.caseUtil import T0T1T2Breached, T3Breached, assign_cases, merge_case, split_cases, transfer_cases
from accounts.errors import serialer_error
from accounts.groups import F_ADMIN, S_ADMIN, CM_group, CR_group, CT_group, get_group_permissions
from drf_yasg import openapi
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from io import StringIO
import csv
from rest_framework import serializers
import pandas as pd
from django.db.models.query import QuerySet
from django.core.exceptions import MultipleObjectsReturned
from django.core.cache import cache
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_INTEGER
import os
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import mixins, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.utils import current_time
from django.db import IntegrityError, models
from django.db import models, transaction
from django.db import models,transaction
from django.apps import apps
from collections import defaultdict
from .models import Notification, NotificationLog, Role, UploadedFile_S3, User_Profilepic, UserRoleFactory
from accounts.permissions import hasincentivespermission
from django.shortcuts import render, get_object_or_404
from django.core.signing import BadSignature, SignatureExpired
from accounts.broadcastViews import translate_text
from accounts.constants import ActionTypes, ConstantVars, Gender, UserRole, CaseStatus, ReportingMedium, Status, CaseNature, \
    ViewLogsIdentifier, CaseActiveStatus, Language, scheduleType
import base64
from accounts.models import (
    SMSTemplates,
    Case,
    CaseReslovingReport,
    Complainer,
    Factory,
    TatawebhooksLog,
    AwarenessProgram,
    FactoryDepartment,
    BroadcastMessage,
    AuditLog,
    BaseUserModel,
    Company,
    scheduleInformation,
    Incentives
)

from accounts.serializers import (
    CaseFileUploadSerializer,
    BaseUserModelSerializer,
    CompanyFactoryPostSerializer,
    CompanySerializer,
    CsvSerializer,
    TemplateSerializer,
    BroadcastMessageSerializer,
    StartInputSerializer,
    FinishInputSerializer,
    GetInputSerializer
)
from accounts.serializers import (
    CaseReopenSerializer,
    CaseResolvingReportUploadSerializer,
    CaseManQCSerializer,
    QCCaseReopenSerializer,
    CaseRepQCSerializer,
    CaseReportSerializers,
    CaseSerializers,
    CaseTrbQCSerializer,
    CaseUploadSerializer,
    FactorySerializer,
    QCReviewSerializer,
    ResetPasswordEmailSerializer,
    SetNewPasswordSerializer,
    SMSTemplatesSerializer,
    AwarenessProgramSerializer,
    FactoryDepartmentSerializer,
    ComplainerSerializer,
    CaseResolvingReportSerializer,
    CaseResolvingReportAdminSerializer

)

    # AuditLog
from accounts.permissions import HasGroupPermission, isSuperAdmin, isSAorRA

from accounts.serializers import CaseFileUploadSerializer,  \
    BaseUserModelSerializer, ChangePasswordSerializer, CompanyFactoryPostSerializer, \
     CompanySerializer,\
     TemplateSerializer
from accounts.serializers import   CaseReopenSerializer, CaseResolvingReportUploadSerializer, \
    CaseManQCSerializer, QCCaseReopenSerializer, \
    CaseRepQCSerializer, CaseReportSerializers, CaseSerializers, CaseTrbQCSerializer, \
     CaseUploadSerializer, FactorySerializer, \
    QCReviewSerializer, ResetPasswordEmailSerializer, \
    SetNewPasswordSerializer, SMSTemplatesSerializer

from rest_framework import permissions
from rest_framework import exceptions
from django.contrib.auth.decorators import user_passes_test
from accounts.dateUtils import working_days

# views.py
@api_view(['POST'])
@csrf_exempt
@transaction.atomic
def sns_webhook(request):
    try:
        sns_message = json.loads(request.body.decode('utf-8'))

        TopicArn='arn:aws:sns:ap-south-1:300380748892:Test_Topic'
        # send_logs_to_cloudwatch(log_group_name, log_stream_name, logs)
        print(sns_message)
        sns_message= json.loads(sns_message['Message'])
        
        print(type(sns_message))
        # Create an instance of SESEmailSender
        
        aws= AwsUtil(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SES_REGION_NAME)
        # Compose the email
        sender_email = 'no-reply@inache.co'
        print("sns_message eqkjrnekj", sns_message)
        recipient_emails = sns_message.get('emailList', None)
        subject = sns_message.get('subject', None)
        notification = sns_message.get('notification', None)
        body_html = sns_message.get('message', None)
        notification = sns_message.get('notification', None)
        print(recipient_emails,body_html,subject)
        logs = { "send_to" : recipient_emails, "send_from" : sender_email }
        event_identifier= sns_message.get('event_identifier', None)
        print("while creating log",type(event_identifier))
        print(sns_message.get('attachment'),"dasdsad ")
        aws.send_email_via_ses(sender_email, recipient_emails, subject, body_html)
        NotificationLog.objects.create(notification_fk=Notification.objects.get(id=notification),message_subject=subject,message_content=body_html,template_fk=Notification.objects.get(id=notification).template_fk,sns_topic_name="Test Topic",notification_type="email", log=logs, event_identifier=event_identifier)

        return HttpResponse("Email Sent",status=200)
    except Exception as e:
        # Handle exceptions or log errors
        
        print(e)
        traceback.print_exc()

        return HttpResponse(status=500)

# Create your views here.
def sendcasemessage(templateID:str, body:str, number:str, company:Company)->int:
    senderid = company.SenderID

    sid = "HXIN1739327617IN"
    api_key = "Ad434b1d76f34c53b443f89df7b3960a5"
    header = {
        "api-key": api_key
    }
    payload = {
        'to': '+91' + number,
        'sender': senderid,
        'source': 'API',
        "type": "TXN",
        "body": body,
        "template_id": templateID
    }
    req = requests.post("https://api.kaleyra.io/v1/" + str(sid) + "/messages", json=(payload), headers=header)
    return req.status_code


# class BUMList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = BaseUserModel.objects.all()
#     serializer_class = BaseUserModelSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class BUMDetailsAV(generics.RetrieveUpdateDestroyAPIView):
#     queryset = BaseUserModel.objects.all()
#     serializer_class = BaseUserModelSerializer
#     # permission_classes=[IsAuthenticated]

class CaseListFilter(generics.ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializers
    name = 'cases-list'

    filter_fields = (
        'CaseManager',
        'CaseTroubleShooter',
        'CaseReporter'
    )




@swagger_auto_schema(method='post', request_body=CaseUploadSerializer)
@api_view(['POST'])
def CaseUploadAV(request:Request)->Response:
    CaseUploadAV.required_groups = {
        'POST': ['CR','CM','CT'],
    }
    CaseUploadAV.model = "case"
    permission_classes =[HasGroupPermission.has_permission(None,request, CaseUploadAV)]
    if request.method == 'POST':
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        serializer = CaseUploadSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            case = serializer.save()
            factory = Factory.objects.get(id=request.data["Factory"])
            casenumber = (
                    ConstantVars.INACHE + factory.region.Name[0] + factory.Code + str(case.id)
            )
            case.CaseNumber = casenumber
            case.T1vrfDate = current_time()
            case.Breached = None
            case.save()
            auditlog = AuditLog.objects.create(
                case=case,
                status=case.CaseStatus,
                created_by=userRole,
                prev_state=str(case),
                current_state=str(case),
                action_type="Case Uploaded - CREATE",
            )
            case.CaseStatus = CaseStatus.ASSIGNED_TO_REPORTER
            if "PhoneNo" in request.data and len(request.data['PhoneNo']) > 0:
                try:
                    comp = Complainer.objects.get(PhoneNo=request.data['PhoneNo'])#, Company=factory.Company,
                                          #Factory=factory)
                    comp.is_active = True
                    comp.Company=factory.Company
                    comp.Factory=factory
                    comp.save()
                    case.Complainer = comp
                except Complainer.DoesNotExist:
                    # if Complainer.objects.filter(PhoneNo=request.data['PhoneNo'],Company=factory.Company).exists():
                    #     print(
                    #         "Cannot register your Case since this number is registered to a different factory"
                    #     )
                    #     return Response(
                    #         {
                    #             "errorMessage": "Cannot register your Case since this number is registered to a different factory"
                    #         },
                    #         status=status.HTTP_404_NOT_FOUND,
                    #     )   
                    # elif Complainer.objects.filter(PhoneNo=request.data['PhoneNo']).exists():
                    #     print(
                    #         "Cannot register your Case since this number is registered to a different company"
                    #     ) 
                    #     return Response(
                    #         {
                    #             "errorMessage": "Cannot register your Case since this number is registered to a different company"
                    #         },
                    #         status=status.HTTP_404_NOT_FOUND,
                    #     )    
                    complainer = Complainer.objects.create(PhoneNo=request.data['PhoneNo'],
                                                           Company=Company.objects.get(id=request.data['Company']),
                                                           Factory=Factory.objects.get(id=request.data['Factory']))
                    case.Complainer = complainer
                body = sendCategoryMessage(case,"Registration Message")
                acklog = AuditLog.objects.create(
                case=case,
                status=case.CaseStatus,
                created_by=userRole,
                prev_state=str(case),
                current_state=str(case),
                message=body,
                action_type="Acknowledgement Message Sent - POST",
            )
            case.save()
            # c=Case.objects.get(CaseNumber=casenumber)
            if userRole.role.role == "CR":
                cr = UserRoleFactory.objects.get(pk=userRole.id)
                case.CaseReporter = cr
            else:
                ret = assigncR(case.CaseNumber)
                case.CaseReporter = ret
            case.save()
            # case.save()



            data['response'] = "Case Upload Successful"
            data['CaseNumber'] = case.CaseNumber
            # data['CaseReporter']=case.CaseReporter.email


        else:
            data = serializer.errors

        return Response(data)


class CaseCreatorFileAV(generics.CreateAPIView):
    # queryset = Case.objects.all()
    permission_classes = [HasGroupPermission]
    serializer_class = CaseFileUploadSerializer
    required_groups = {
        'POST': ['CR','CM','CT'],
    }
    model = "case"
    def perform_create(self:Request, serializer)->Response:
        userRole=parser(self.request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        # CaseFileUploadSerializer(data=self.request.data)
        # CaseFileupload=self.request.data['CaseFileupload'],Factory_id=self.request.data['Factory'],CommentsByRep=self.request.data['CommentsByRep'],ReportingMedium=self.request.data['ReportingMedium'],Company_id=self.request.data['Company'],MessagebyWorker=self.request.data['MessagebyWorker']
        case = serializer.save()
        data = {}
        factory = Factory.objects.get(id=self.request.data["Factory"])
        casenumber = (
                ConstantVars.INACHE + factory.region.Name[0] + factory.Code + str(case.id)
        )

        case.CaseNumber = casenumber
        case.T1vrfDate = current_time()
        case.Breached = None
        case.save()
        auditlog = AuditLog.objects.create(
            case=case,
            status=case.CaseStatus,
            created_by=userRole,
            prev_state=str(case),
            current_state=str(case),
            action_type="Case Uploaded - CREATE",
        )
        case.CaseStatus = CaseStatus.ASSIGNED_TO_REPORTER
        if "PhoneNo" in self.request.data and len(self.request.data["PhoneNo"]) > 0:
            try:
                comp = Complainer.objects.get(PhoneNo=self.request.data['PhoneNo'])#, Company=company,
                #Factory=factory)
                comp.is_active = True
                comp.Company=factory.Company
                comp.Factory=factory
                comp.save()
                case.Complainer = comp

            except Complainer.DoesNotExist:
                # if Complainer.objects.filter(PhoneNo=self.request.data['PhoneNo'],Company=factory.Company).exists():
                #     print(
                #         "Cannot register your Case since this number is registered to a different factory"
                #     )
                #     return HttpResponse(
                #         "Cannot register your Case since this number is registered to a different factory"
                #     )   
                # elif Complainer.objects.filter(PhoneNo=self.request.data['PhoneNo']).exists():
                #     print(
                #         "Cannot register your Case since this number is registered to a different company"
                #     )  
                #     return HttpResponse(
                #         "Cannot register your Case since this number is registered to a different company"
                #     ) 
                complainer = Complainer.objects.create(PhoneNo=self.request.data['PhoneNo'],
                                                       Company=Company.objects.get(id=self.request.data['Company']),
                                                       Factory=Factory.objects.get(id=self.request.data['Factory']))
                case.Complainer = complainer
            body = sendCategoryMessage(case,"Registration Message")
            acklog = AuditLog.objects.create(
                case=case,
                status=case.CaseStatus,
                created_by=userRole,
                prev_state=str(case),
                current_state=str(case),
                message=body,
                action_type="Acknowledgement Message Sent - POST",
            )
        case.save()
        if userRole.role.role == UserRole.CASE_REPORTER:
            cr = UserRoleFactory.objects.get(pk=userRole.id)
            case.CaseReporter = cr
            case.save()
        else:
            ret = assigncR(case.CaseNumber)
            case.CaseReporter = ret
            case.save()
        case.CaseValidation = True
        case.save()

        data['response'] = "Case Upload Successful"
        data['CaseNumber'] = case.CaseNumber

        return Response(data)


class CaseResolveAV(APIView):
    permission_classes=[HasGroupPermission]
    required_groups = {
    'GET': ['CT','REGIONAL_ADMIN', 'SUPER_ADMIN'],
    'PUT': ['CT','REGIONAL_ADMIN'],
    'POST':['CT','REGIONAL_ADMIN'],
    #'PATCH': ['CT']
    }
    model = "casereslovingreport"

    def get(self, request: Request) -> Response:
        caseID = request.query_params.get("caseID")
        caseObj = Case.objects.get(id=caseID)
        try:
            ccReport = CaseReslovingReport.objects.get(Case=caseID)
            ccReportSerializer = CaseResolvingReportSerializer(ccReport)
            draftObj = BroadcastMessage.objects.filter(status=Status.CTDRAFT,sendCount=caseID)
            if caseObj.CurrentStatus == CaseActiveStatus.DRAFT and (draftObj.exists() == True):
                data = ccReportSerializer.data
                company = request.user.company_fk.id
                draft = draftObj.latest("lastModified")
                serializer = BroadcastMessageSerializer(draft)
                values = serializer.data
                variables = json.loads(SMSTemplates.objects.get(templateID=serializer.data["templateIDs"][0],Company=company).variables)
                inputs = serializer.data["inputVariables"]
                list = []
                for key,value in variables.items():
                    list.append({"var":{key:value},"InputValue":inputs[value],"language":serializer.data['Languages']})

                message = {
                                "message": "Case Resolving Report for caseID {} has been fetched successfully".format(
                                    request.query_params.get("caseID")
                                ),
                                "message_body": {"CCRWhen":data["CCRWhen"],"CCRWhathappened":data["CCRWhathappened"],"CCRWhere":data["CCRWhere"],"CCRWho":data["CCRWho"],"CCRremarks":data["CCRremarks"],"CCTemplate":values["templateTitle"],"CCLanguage":values["Languages"][0],"variables":list,"CCMessage":values["messageBody"][0]["body"]},
                            }
                return Response(message, status=status.HTTP_200_OK)
            else:

                message = {
                    "message": "Case Resolving Report for caseID {} has been fetched successfully".format(
                        request.query_params.get("caseID")
                    ),
                    "message_body": ccReportSerializer.data,
                        }
                return Response(message, status=status.HTTP_200_OK)
        except:
            return Response({'Error': "Case Resolving Report Not found"}, status=status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def post(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        caseObj = Case.objects.get(id=request.data["Case"])
        if request.query_params.get('Method') == Status.SENT:
            # context={"Message":request.data['CCMessage']}
            # del request.data['CCMessage']
            if caseObj.Complainer is not None:
                if caseObj.T3vrfDate is None and caseObj.CaseCategory != "POSH":
                    return Response(
                    {
                        "errorMessage": "Please send Acknowledgement Message to Resolve the Report"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            if userRole.role.role == UserRole.CASE_TROUBLESHOOTER:
                serializer = CaseResolvingReportUploadSerializer(data=request.data,
                                                                #  context=context
                                                                )
            elif userRole.role.role == UserRole.REGIONAL_ADMIN:
                serializer = CaseResolvingReportAdminSerializer(data=request.data,
                                                                #  context=context
                                                                ) 
            data = {}
            if serializer.is_valid(): 
                if userRole is None:
                    return Response({"error":"ROLE ID NOT PRESENT"})
                user_id = userRole.id
                cache_key = f'user_data_{user_id}_first'
                cacheData = cache.get(cache_key)
                # if (caseObj.Complainer):
                #     # template = SMSTemplates.objects.get(templateID=request.data['CCTemplateID'])
                #     try:
                #         template=SMSTemplates.objects.get(templateID=request.data['CCTemplateID'])
                #     except MultipleObjectsReturned:
                #         template=SMSTemplates.objects.filter(templateID=request.data['CCTemplateID']).first()
                #     code = sendcasemessage(template.templateID, request.data['CCMessage'],
                #                         str(caseObj.Complainer.PhoneNo), caseObj.Company)

                if caseObj.Complainer:
                    try:
                        template = SMSTemplates.objects.get(
                            templateID=request.data["CCTemplateID"],Company=request.data["Company"]
                        )
                    except:
                        return Response(
                            {
                                "errorMessage": "Please complete Resolving Message"
                                },
                                status=status.HTTP_404_NOT_FOUND,
                                )
                    if cacheData != None and int(cacheData['caseID']) == request.data["Case"]:
                        if cacheData['done'] == "No":
                            return Response(
                                {
                                    "errorMessage": "Please complete Resolving Message Process"
                                    },
                                    status=status.HTTP_404_NOT_FOUND,
                                    )
                # print(case_resolving_report.Case.Company, "DFASDASDASDSADASDASDASDASDASD")
                    code = sendcasemessage(
                        template.templateID,
                        request.data["CCMessage"],
                        str(caseObj.Complainer.PhoneNo),
                        caseObj.Company,
                    )
                    # action_type={UserRole.CASE_TROUBLESHOOTER:"Case Resolving Message Sent by CT - POST",UserRole.REGIONAL_ADMIN:{"Resolving Message":"Case Resolving Message Sent by RA - POST","Closing Message":"Case Closed by RA - POST","UNRESPONSIVE_MESSAGE_SENT" :"Case Closed Due to Lack of Response,Message sent by RA - POST"}}
                    # action_type.get(userRole.role.role)
                    case_resolving_report = serializer.save()
                    if userRole.role.role==UserRole.CASE_TROUBLESHOOTER:
                        state = "resolved"
                        auditlog = AuditLog.objects.create(
                            case=case_resolving_report.Case,
                            status=CaseStatus.RESOLVED,
                            created_by=userRole,
                            prev_state="",
                            current_state="",
                            message=request.data["CCMessage"],
                            action_type=ActionTypes.CASE_RESOLVING_MESSAGE_SENT,
                        )
                    elif userRole.role.role==UserRole.REGIONAL_ADMIN:
                        if "Resolving Message" in template.template_categories:
                            state = "resolved"
                            auditlog = AuditLog.objects.create(
                                case=case_resolving_report.Case,
                                status=CaseStatus.RESOLVED,
                                created_by=userRole,
                                prev_state="",
                                current_state="",
                                message=request.data["CCMessage"],
                                action_type=ActionTypes.CASE_RESOLVING_MESSAGE_SENT,
                            )
                        elif "Closing Message" in template.template_categories or "Posh Message" in template.template_categories:
                            state = "closed"
                            auditlog = AuditLog.objects.create(
                                case=case_resolving_report.Case,
                                status=CaseStatus.CLOSED,
                                created_by=userRole,
                                prev_state="",
                                current_state="",
                                message=request.data["CCMessage"],
                                action_type=ActionTypes.CASE_CLOSING_MESSAGE_SENT,
                            )
                        elif "Unresponsive Message" in template.template_categories or "Posh Unresponsive Message" in template.template_categories:
                            state = "Unresponsive"
                            auditlog = AuditLog.objects.create(
                                case=case_resolving_report.Case,
                                status=CaseStatus.UNRESPONSIVE,
                                created_by=userRole,
                                prev_state="",
                                current_state="",
                                message=request.data["CCMessage"],
                                action_type=ActionTypes.UNRESPONSIVE_MESSAGE_SENT,
                            )
                                         
                else:
                    state = "resolved"
                    case_resolving_report = serializer.save()
                cache.delete(cache_key)
                cacheData=None
                return Response(
                    "Success, Case: " + str(case_resolving_report.Case.CaseNumber) + " is " + state
                )
            else:
                return Response(serializer.errors)

        elif request.query_params.get('Method') == Status.DRAFT:
            serializer = CaseResolvingReportSerializer(data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                caseresreport = serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            userRole=parser(request)
            if userRole is None:
                return Response({"error":"ROLE ID NOT PRESENT"})
            user_id = userRole.id
            cache_key = f'user_data_{user_id}_first'
            data = cache.get(cache_key)
            caseObj.CurrentStatus = CaseActiveStatus.DRAFT
            caseObj.save()
            if data != None and int(data['caseID']) == request.data["Case"]:
                message = data['templates']
                body = []
                templateIDs = []
                for templates in message:
                    body.append(templates)
                    templateIDs.append(templates["templateID"])
                if data['done'] == "No":
                    variables = data['variables']
                    values = {}
                    for key,value in variables.items():
                        values[value] = ""
                    data['inputs']=values
                draft = BroadcastMessage.objects.create(
                    createdBy =  request.user.user_name + " (" + userRole.role.role + ")",
                    Languages = data['language'],
                    templateTitle = message[0]["Title"],
                    messageBody = body,
                    factories = data['factories'],
                    status = Status.CTDRAFT,
                    templateIDs = list(set(templateIDs)),
                    inputVariables = data['inputs'],
                    sendCount = data['caseID']
                )
                draft.save()
                cache.delete(cache_key)  # Delete data from cache
                data = None
                serializer = BroadcastMessageSerializer(draft)
                message = {
                    "message": "Success, Case: " + str(caseresreport.Case.CaseNumber) + " Draft is saved",
                    "message_body": serializer.data,
                }
                return Response(message, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    "Success, Case: " + str(caseresreport.Case.CaseNumber) + " draft is saved"
                )

    @transaction.atomic
    def put(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        caseresreport = CaseReslovingReport.objects.get(pk=request.data['Case'])
        caseObj = Case.objects.get(id=request.data["Case"])
        if request.query_params.get('Method') == Status.SENT:
            if caseObj.Complainer is not None:
                if caseObj.T3vrfDate is None and caseObj.CaseCategory != "POSH":
                    return Response(
                        {
                            "errorMessage": "Please send Acknowledgement Message to Resolve the Report"
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )
            if userRole.role.role == UserRole.CASE_TROUBLESHOOTER:
                serializer = CaseReportSerializers(caseresreport,data=request.data,
                                                                #  context=context
                                                                )
            elif userRole.role.role == UserRole.REGIONAL_ADMIN:
                serializer = CaseResolvingReportAdminSerializer(caseresreport,data=request.data,
                                                                #  context=context
                                                                ) 
            if serializer.is_valid():
                if userRole is None:
                    return Response({"error":"ROLE ID NOT PRESENT"})
                user_id = userRole.id
                cache_key = f'user_data_{user_id}_first'
                cacheData = cache.get(cache_key)
                if caseObj.Complainer:
                    try:
                        template = SMSTemplates.objects.get(
                            templateID=request.data["CCTemplateID"], Company=request.data["Company"]
                        )
                    except:
                        return Response(
                            {
                                "errorMessage": "Please complete Resolving Message"
                                },
                                status=status.HTTP_404_NOT_FOUND,
                                )
                    if cacheData != None and int(cacheData['caseID']) == request.data["Case"]:
                        if cacheData['done'] == "No":
                            return Response(
                                {
                                    "errorMessage": "Please complete Resolving Message Process"
                                    },
                                    status=status.HTTP_404_NOT_FOUND,
                                    )
                    code = sendcasemessage(
                        template.templateID,
                        request.data["CCMessage"],
                        str(caseObj.Complainer.PhoneNo),
                        caseObj.Company,
                    )
                    caseresreport = serializer.save()
                    draftObj = BroadcastMessage.objects.filter(status=Status.CTDRAFT,
                                                                sendCount=request.data["Case"])
                    if draftObj.exists():
                        draftObj.delete()
                    if userRole.role.role==UserRole.CASE_TROUBLESHOOTER:
                        state = "resolved"
                        auditlog = AuditLog.objects.create(
                            case=caseresreport.Case,
                            status=CaseStatus.RESOLVED,
                            created_by=userRole,
                            prev_state="",
                            current_state="",
                            message=request.data["CCMessage"],
                            action_type=ActionTypes.CASE_RESOLVING_MESSAGE_SENT,
                        )
                    elif userRole.role.role==UserRole.REGIONAL_ADMIN:
                        if "Resolving Message" in template.template_categories:
                            state = "resolved"
                            auditlog = AuditLog.objects.create(
                                case=caseresreport.Case,
                                status=CaseStatus.RESOLVED,
                                created_by=userRole,
                                prev_state="",
                                current_state="",
                                message=request.data["CCMessage"],
                                action_type=ActionTypes.CASE_RESOLVING_MESSAGE_SENT,
                            )
                        elif "Closing Message" in template.template_categories or "Posh Message" in template.template_categories:
                            state = "closed"
                            auditlog = AuditLog.objects.create(
                                case=caseresreport.Case,
                                status=CaseStatus.CLOSED,
                                created_by=userRole,
                                prev_state="",
                                current_state="",
                                message=request.data["CCMessage"],
                                action_type=ActionTypes.CASE_CLOSING_MESSAGE_SENT,
                            )
                        elif "Unresponsive Message" in template.template_categories or  "Posh Unresponsive Message" in template.template_categories:
                            state = "Unresponsive"
                            auditlog = AuditLog.objects.create(
                                case=caseresreport.Case,
                                status=CaseStatus.UNRESPONSIVE,
                                created_by=userRole,
                                prev_state="",
                                current_state="",
                                message=request.data["CCMessage"],
                                action_type=ActionTypes.UNRESPONSIVE_MESSAGE_SENT,
                            )
                else:
                    state = "resolved"
                    caseresreport = serializer.save()
                cache.delete(cache_key)
                cacheData=None
                return Response(
                    "Success, Case: " + str(caseresreport.Case.CaseNumber) +  " is " + state
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.query_params.get('Method') == Status.DRAFT:
            caseresreport = CaseReslovingReport.objects.get(pk=request.data['Case'])
            serializer = CaseResolvingReportSerializer(caseresreport, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                caseresreport = serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            userRole=parser(request)
            if userRole is None:
                return Response({"error":"ROLE ID NOT PRESENT"})
            user_id = userRole.id
            cache_key = f'user_data_{user_id}_first'
            data = cache.get(cache_key)
            caseObj.CurrentStatus = CaseActiveStatus.DRAFT
            caseObj.save()
            if data != None and int(data['caseID']) == request.data["Case"]:
                message = data['templates']
                templateIDs = []
                body = []
                for templates in message:
                    body.append(templates)
                    templateIDs.append(templates["templateID"])
                if data['done'] == "No":
                    variables = data['variables']
                    values = {}
                    for key,value in variables.items():
                        values[value] = ""
                    data['inputs']=values
                draftObj = BroadcastMessage.objects.filter(status=Status.CTDRAFT, sendCount=request.data["Case"])
                if draftObj.exists():
                    draft = draftObj.latest("lastModified")
                    serializer = BroadcastMessageSerializer(draft)
                    draftSerializer = serializer.data
                    draftSerializer["lastModified"] = current_time()
                    draftSerializer["Languages"] = data['language']
                    draftSerializer["messageBody"] = data['templates']
                    draftSerializer["templateIDs"] = list(set(templateIDs))
                    draftSerializer["inputVariables"] = data['inputs']
                    draftSerializer["Genders"] = ["None"]
                    draftSerializer["departments"] = ["None"]
                    serializer = BroadcastMessageSerializer(
                        draft, data=draftSerializer, partial=True
                    )
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                else:
                    draft = BroadcastMessage.objects.create(
                        createdBy=request.user.user_name + " (" + userRole.role.role + ")",
                        Languages=data['language'],
                        templateTitle=message[0]["Title"],
                        messageBody=body,
                        Factory=Factory.objects.get(id=data['factory']),
                        status=Status.CTDRAFT,
                        templateIDs=list(set(templateIDs)),
                        inputVariables=data['inputs'],
                        sendCount=data['caseID']
                    )
                    draft.save()
                    serializer = BroadcastMessageSerializer(draft)
                cache.delete(cache_key)  # Delete data from cache
                data = None
                message = {
                    "message": "Success, Case: " + str(caseresreport.Case.CaseNumber) + " Draft is updated",
                    "message_body": serializer.data,
                }
                return Response(message, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    "Success, Case: " + str(caseresreport.Case.CaseNumber) + " draft is updated"
                )
        # except KeyError as ke:
        #      return Response(
        #         {
        #             "errorMessage": "Key Not Found in the data" + str(ke)
        #         },
        #         status=status.HTTP_404_NOT_FOUND,
        #     )



@swagger_auto_schema(method='post', request_body=QCCaseReopenSerializer)
@api_view(['POST'])
def QCCaseReopenAV(request:Request)->Response:
    if request.method == 'POST':
        # print(self.kwargs['pk'])
        serializer = QCCaseReopenSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            case = serializer.save()
            data['response'] = "Case Reopened Successful"
        else:
            data = serializer.errors
        return Response(data)


class CaseSLAReopenAV(APIView):
    permission_classes=[HasGroupPermission]
    required_groups = {
    'POST':['CT','REGIONAL_ADMIN'],
    }
    model = "case"
    @swagger_auto_schema(request_body=CaseReopenSerializer)
    @transaction.atomic
    def post(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        case = Case.objects.get(id=request.data['Case'])
        cc = case.ResolveTime
        cc = cc.replace(tzinfo=None)
        now = datetime.datetime.now()
        rem = now - cc
        data = {}
        if (rem.total_seconds() > 72 * 3600):
            serializer = CaseReopenSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                reopencase = serializer.save()
                data["response"] = "Case " + str(reopencase.Case.CaseNumber) + " Reopened"
                auditlog = AuditLog.objects.create(
                    case=reopencase.Case,
                    status=reopencase.Case.CaseStatus,
                    created_by=userRole,
                    prev_state=str(reopencase.Case),
                    current_state=str(reopencase.Case.CaseNumber + "_1"),
                    # message="Case demoted to under investigation due to complainant unsatisfaction",
                    action_type="Case Reopened - (New Case Made)- PUT",
                )
                auditlog = AuditLog.objects.create(
                    case=case,
                    status=case.CaseStatus,
                    created_by=userRole,
                    prev_state=str(reopencase),
                    current_state=str(case),
                    action_type="Case Uploaded - CREATE",
                )
            else:
                data = serializer.errors
        else:
            if userRole.role.role==UserRole.CASE_TROUBLESHOOTER:
                AuditLog.objects.create(
                    case=case,
                    status=case.CaseStatus,
                    created_by=userRole,
                    prev_state=str(case),
                    current_state=str(case),
                    # message="Case demoted to under investigation due to complainant unsatisfaction",
                    action_type=ActionTypes.CASE_REOPENED_CT,
                )
                # case.Counter = 4
                case.CaseStatus = CaseStatus.RE_INVESTIGATION
                case.reopened = True
                if case.Complainer is not None:
                    case.T3vrfDate = current_time()
                else:
                    case.T2vrfDate = current_time()
                newstate = case.save()
                data["response"] = (
                    "Case " + str(case.CaseNumber) + " is Under ReInvestigation"
                )
            elif userRole.role.role==UserRole.REGIONAL_ADMIN:
                AuditLog.objects.create(
                    case=case,
                    status=case.CaseStatus,
                    created_by=userRole,
                    prev_state=str(case),
                    current_state=str(case),
                    # message="Case demoted to under investigation due to complainant unsatisfaction",
                    action_type=ActionTypes.CASE_REOPENED_RA,
                )
                # case.Counter = 4
                case.CaseStatus = CaseStatus.RE_INVESTIGATION_RA
                case.reopened = True
                case.T3vrfDate = current_time()
                newstate = case.save()
                data["response"] = (
                    "Case " + str(case.CaseNumber) + " is Under ReInvestigation"
                )
        return Response(data)


@api_view(['POST'])
def logout_view(request:Request)->Response:
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(data="logout sucessful", status=status.HTTP_200_OK)


class CompanyListAV(generics.ListCreateAPIView):
    # permission_classes = [AdminOnly]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetailsAV(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyFactoryPost(generics.CreateAPIView):
    serializer_class = CompanyFactoryPostSerializer

    def perform_create(self, serializer):
        pk = self.kwargs['c']
        Com = Company.objects.get(pk=pk)
        serializer.save(Company=Com)

class CaseRepListAV(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = BaseUserModelSerializer

    def get_queryset(self):
        c = self.kwargs['c']
        f = self.kwargs['f']
        userRoles=UserRoleFactory.objects.filter(role__role=UserRole.CASE_REPORTER,user_fk__company_fk=c,factory_fk=f,is_active=True)
        user_ids = userRoles.values('user_fk_id').distinct()

        return BaseUserModel.objects.filter(id__in=user_ids)

            
class QCNewCaseListAV(generics.ListAPIView):
    serializer_class = CaseSerializers

    def get_queryset(self):
        c = self.kwargs["c"]
        f = self.kwargs["f"]
        # ct = self.kwargs['ct']
        # update the counter value and polssibly delete the counter because qc will se all the cases not resolved cases only
        return Case.objects.filter(
            Company=c, Factory=f, Counter__in=["5", "6"]
        )  # .order_by( ca( When ( ReportingMedium="", then=Value(0) ),When ( ReportingMedium="Call", then=Value(1)  ),When ( ReportingMedium="In Person", then=Value(2)  ),When ( ReportingMedium="Suggestion Box", then=Value(3)  ),When ( ReportingMedium="Worker Committee", then=Value(4)  ),default = Value(5)))


class CaseTotalAV(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CaseSerializers

    def get_queryset(self):
        case = Case.objects.all()
        return case

def get_months_between_dates(start_date, end_date):
    months = []
    while start_date <= end_date:
        months.append(start_date.strftime('%Y-%m'))
        start_date += timedelta(days=32)
        start_date = start_date.replace(day=1)
    return months

def get_cumulative_awareness(request,months,awareness,requiredPrograms):
    minRequired=0
    for month_str in months:
        month = int(month_str.split('-')[1])
        year = int(month_str.split('-')[0])
        check = awareness.filter(Q(Date__year=year) & Q(Date__month=month))
        if check.exists():
            minRequired += check.latest("id").programStatus["Required"]
        else:
            if current_time().month == month:
                minRequired += requiredPrograms
            else:
                minRequired += 4
    return minRequired


class CaseSepCount(APIView):
    permission_classes = [hasincentivespermission]

    def post(self, request: Request) -> Response:
        company = request.data["Company"]
        factory = request.data["Factory"]
        # the first step takes the from and to dates to filter cases
        if request.data['from'] and request.data['to']:
            data = request.data
            tartDate = data['from']
            startDate = datetime.datetime.strptime(tartDate, '%Y-%m-%d')
            ndDate = data['to']
            endDate = datetime.datetime.strptime(ndDate, '%Y-%m-%d')

        # if dates are not given, it will filter through last 30 days
        else:
            startDate = date.today() - timedelta(days=30)
            endDate = date.today() 


        case = Case.objects.filter(
            Date__date__gte=startDate, Date__date__lte=endDate, Factory=factory, Company=company, CaseValidation = True
        )  # cases on given dates
        
        requiredPrograms = Factory.objects.get(id=factory).requiredAwarenessProgram
        awareness = AwarenessProgram.objects.filter(Factory=factory)
        months = get_months_between_dates(startDate,endDate)
        minimumPrograms = get_cumulative_awareness(request,months,awareness,requiredPrograms)

        programs = AwarenessProgram.objects.filter(Q(Factory=factory) & Q(Date__date__gte=startDate) & Q(Date__date__lte=endDate) & Q(Breached=False)).count()

        # the condition to check if there are any closed or resolved cases when filtered
        if case.filter(Q(CaseStatus=CaseStatus.CLOSED) | Q(CaseStatus=CaseStatus.RESOLVED)):
            rescases = case.filter(CaseStatus=CaseStatus.RESOLVED).count()
            clscases = case.filter(CaseStatus=CaseStatus.CLOSED).count()
            procases = case.exclude(Q(CaseStatus=CaseStatus.CLOSED) | Q(CaseStatus=CaseStatus.RESOLVED)).count()
            resclscases = case.filter(Q(CaseStatus=CaseStatus.CLOSED) | Q(CaseStatus=CaseStatus.RESOLVED))
            cases = resclscases.filter(Breached=False).count()  # cases are eligible if nothing is breached
            chk = resclscases.count()
            Discases = chk - cases
            t00 = resclscases.filter(T0Breached=False).count()
            t01 = resclscases.filter(T0Breached=True).count()
            t10 = resclscases.filter(T1Breached=False).count()
            t11 = resclscases.filter(T1Breached=True).count()
            t20 = resclscases.filter(T2Breached=False).count()
            t21 = resclscases.filter(T2Breached=True).count()
            t30 = resclscases.filter(T3Breached=False).count()
            t31 = resclscases.filter(T3Breached=True).count()
            a10 = resclscases.filter(t3a1=False).count()
            a11 = resclscases.filter(t3a1=True).count()
            a20 = resclscases.filter(t3a2=False).count()
            a21 = resclscases.filter(t3a2=True).count()
            b10 = resclscases.filter(t3b1=False).count()
            b11 = resclscases.filter(t3b1=True).count()
            b20 = resclscases.filter(t3b2=False).count()
            b21 = resclscases.filter(t3b2=True).count()
            c10 = resclscases.filter(t3c1=False).count()
            c11 = resclscases.filter(t3c1=True).count()
            c20 = resclscases.filter(t3c2=False).count()
            c21 = resclscases.filter(t3c2=True).count()
            percent = (cases / chk) * 100  # percentage of eligible cases
            recases = case.filter(reopened=True).count()
            nonrecases = chk
            repercent = (recases / (chk + recases)) * 100  # percentage of reopened cases
            nonrepercent = 100.0 - repercent
            # if the factory satisfies all the 3 conitions, then it is eligible
            if percent == 100.0 and repercent <= 10 and chk >= 3 and programs >= minimumPrograms:
                eligible = True
                # eligible={"Case compliance rate":percent,"QC case reopen rate":repercent,"Closed/Resolved cases":chk}
                noteligible = False
            else:
                eligible = False
                noteligible = True
                # noteligible={"Case compliance rate":percent,"QC case reopen rate":repercent,"Closed/Resolved cases":chk}
            return Response({"Cases": {CaseStatus.CLOSED: clscases, CaseStatus.RESOLVED: rescases, "InProcess": procases},
                             "Eligible": {"Qualified": cases, "Disqualified": Discases},
                             "payload": [{"type": "T0", "value": t01, "caseType": "breached"},
                                         {"type": "T0", "value": t00, "caseType": "non-breached"},
                                         {"type": "T1", "value": t11, "caseType": "breached"},
                                         {"type": "T1", "value": t10, "caseType": "non-breached"},
                                         {"type": "T2", "value": t21, "caseType": "breached"},
                                         {"type": "T2", "value": t20, "caseType": "non-breached"},
                                         {"type": "T3", "value": t31, "caseType": "breached"},
                                         {"type": "T3", "value": t30, "caseType": "non-breached"}],
                             "subT": [{"type": "T3a1", "value": a11, "caseType": "breached"},
                                      {"type": "T3a1", "value": a10, "caseType": "non-breached"},
                                      {"type": "T3a2", "value": a21, "caseType": "breached"},
                                      {"type": "T3a2", "value": a20, "caseType": "non-breached"},
                                      {"type": "T3b1", "value": b11, "caseType": "breached"},
                                      {"type": "T3b1", "value": b10, "caseType": "non-breached"},
                                      {"type": "T3b2", "value": b21, "caseType": "breached"},
                                      {"type": "T3b2", "value": b20, "caseType": "non-breached"},
                                      {"type": "T3c1", "value": c11, "caseType": "breached"},
                                      {"type": "T3c1", "value": c10, "caseType": "non-breached"},
                                      {"type": "T3c2", "value": c21, "caseType": "breached"},
                                      {"type": "T3c2", "value": c20, "caseType": "non-breached"}],
                             "factory": {"eligible": eligible, "noteligible": noteligible},
                             "Quality": [{"caseType": "Reopened", "value": recases, "percent": repercent},
                                         {"caseType": "Passed", "value": nonrecases, "percent": nonrepercent}],
                             "Awareness": {"programs":programs,"minRequired":minimumPrograms}})
        # if there are no closed or resolved cases, only return in-progress cases and given all others 0
        else:
            procases = case.exclude(Q(CaseStatus=CaseStatus.CLOSED) | Q(CaseStatus=CaseStatus.RESOLVED)).count()
            return Response({"Cases": {CaseStatus.CLOSED: 0, CaseStatus.RESOLVED: 0, "InProcess": procases},
                             "Eligible": {"Qualified": 0, "Disqualified": 0},
                             "payload": [{"type": "T0", "value": 0, "caseType": "non-breached"},
                                         {"type": "T0", "value": 0, "caseType": "breached"},
                                         {"type": "T1", "value": 0, "caseType": "non-breached"},
                                         {"type": "T1", "value": 0, "caseType": "breached"},
                                         {"type": "T2", "value": 0, "caseType": "non-breached"},
                                         {"type": "T2", "value": 0, "caseType": "breached"},
                                         {"type": "T3", "value": 0, "caseType": "non-breached"},
                                         {"type": "T3", "value": 0, "caseType": "breached"}],
                             "subT": [{"type": "T3a1", "value": 0, "caseType": "non-breached"},
                                      {"type": "T3a1", "value": 0, "caseType": "breached"},
                                      {"type": "T3a2", "value": 0, "caseType": "non-breached"},
                                      {"type": "T3a2", "value": 0, "caseType": "breached"},
                                      {"type": "T3b1", "value": 0, "caseType": "non-breached"},
                                      {"type": "T3b1", "value": 0, "caseType": "breached"},
                                      {"type": "T3b2", "value": 0, "caseType": "non-breached"},
                                      {"type": "T3b2", "value": 0, "caseType": "breached"},
                                      {"type": "T3c1", "value": 0, "caseType": "non-breached"},
                                      {"type": "T3c1", "value": 0, "caseType": "breached"},
                                      {"type": "T3c2", "value": 0, "caseType": "non-breached"},
                                      {"type": "T3c2", "value": 0, "caseType": "breached"}],
                             "factory": {"eligible": False, "noteligible": True},
                             "Quality": [{"caseType": "Reopened", "value": 0, "percent": 0.0},
                                         {"caseType": "Passed", "value": 0, "percent": 0.0}],
                             "Awareness": {"programs":programs,"minRequired":minimumPrograms}})


class FacFilter(APIView):

    def get(self, request: Request) -> Response:
        query_params = request.query_params
        company = query_params.get("company")
        start_date_str = query_params.get("from")
        end_date_str = query_params.get("to")
        Region = query_params.get("region")
        factory = query_params.get("factory")
        q = Q()
        q_fac = Q()
        q_factory = Q()
        q_region = Q()
        q_facfilter = Q()
        q_company = Q(Company=company)
        if start_date_str:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        else:
            start_date = date.today() - timedelta(days=30)
        if end_date_str:
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
        else:
            end_date = date.today() 
        q &= Q(Date__date__gte=start_date)
        q &= Q(Date__date__lte=end_date)
        if factory:
            codes = factory.split(",")
            for div in codes:
                q_factory |= Q(Factory__Code=div)
                q_facfilter |= Q(Code=div)
        if Region:
            division = Region.split(",")
            for div in division:
                if factory == None:
                    name = Factory.objects.filter(region=div) 
                    if name:
                        for na in name:
                            q_factory |= Q(Factory=na.id)
                            q_facfilter |= Q(id=na.id)
                    else:
                        q_factory |= Q(Factory=None)
                        q_facfilter |= Q(id=None)
                else:
                    q_region |= Q(Factory__region=div)
        
        chain = [q, q_region, q_factory, q_company]
        q = reduce(lambda x, y: x & y, [f for f in chain if f is not None])
        # q = Q.reduce(q, q_region, q_factory, q_company)
        facChain = [q_facfilter, q_company]
        q_fac = reduce(lambda x, y: x & y, [f for f in facChain if f is not None])
        # q_fac = Q.reduce(q_facfilter,q_company)
        cas = Case.objects.filter(q)
        factory_filter = Factory.objects.filter(q_fac,is_active=True)
        # {"date factory region", "date factory", "date region", "factory region", "date", "factory", "region", "nothing"}

        tot = cas.count()
        res = cas.filter(CaseStatus=CaseStatus.RESOLVED).count()
        cls = cas.filter(CaseStatus=CaseStatus.CLOSED).count()
        new = cas.filter(CaseStatus__in=[CaseStatus.ASSIGNED_TO_REPORTER]).count()

        rescls = cas.filter(
            Q(CaseStatus=CaseStatus.CLOSED) | Q(CaseStatus=CaseStatus.RESOLVED)
        )

        rsclcnt = rescls.count()
        pro = tot - res - cls - new
        # pro = cas.exclude(Q(CaseStatus=CaseStatus.CLOSED) | Q(CaseStatus=CaseStatus.RESOLVED) | Q(CaseStatus=CaseStatus.ASSIGNED_TO_REPORTER)).count()
        ivr = cas.filter(ReportingMedium=ReportingMedium.CALL).count()
        # sms=rescls.filter(ReportingMedium=ReportingMedium.SMS).count()
        inper = cas.filter(ReportingMedium=ReportingMedium.IN_PERSON).count()
        sb = cas.filter(ReportingMedium=ReportingMedium.SUGGESTION_BOX).count()
        wc = cas.filter(ReportingMedium=ReportingMedium.WORKER_COMMITTEE).count()
        min = rescls.filter(Q(Priority="Minor Grievance (Internal)") | Q(Priority="Minor Grievance (External)")).count()
        med = rescls.filter(

            Q(Priority="Medium Grievance (Internal)")
            | Q(Priority="Medium Grievance (External)")
        ).count()
        maj = rescls.filter(
            Q(Priority="Major Grievance (Level 1)")
            | Q(Priority="Major Grievance (Level 2)")
        ).count()
        low_percentage = 0
        medium_percentage = 0
        high_percentage = 0
        if rsclcnt > 0:
            low_percentage = (min / rsclcnt) * 100
            medium_percentage = (med / rsclcnt) * 100
            high_percentage = (maj / rsclcnt) * 100
        # factory=Factory.objects.all()
        # print(factory)
        elig = 0
        nonelig = 0
        payload = []
        typeT = []
        utilisation_rate = []
        for fac in factory_filter.iterator():
            # print("facid: ",fac.id)
            case = cas.filter(Factory=fac.id)
            case_count = case.count()
            resclscases = case.filter(Q(CaseStatus=CaseStatus.CLOSED) | Q(CaseStatus=CaseStatus.RESOLVED))
            cases = resclscases.filter(Breached=False).count()
            chk = resclscases.count()
            Discases = chk - cases
            t0 = resclscases.filter(T0Breached=False).count()
            t1 = resclscases.filter(T1Breached=False).count()
            t2 = resclscases.filter(T2Breached=False).count()
            t3 = resclscases.filter(T3Breached=False).count()

            # print("chk: ",chk)
            recases = cas.filter(reopened=True).count()
            months = [
                "dummy",
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ]
            workers = [
                "count",
                934,
                934,
                934,
                934,
                934,
                934,
                934,
                934,
                934,
                934,
                934,
                934,
            ]

            for i in range(1, 13):
                case_month = case.filter(Date__month=i).count()
                # print(case_month)
                util_percent = (case_month / workers[i]) * 100

                utilisation_rate.extend(
                    [
                        {
                            "month": months[i],
                            "value": util_percent,
                            "factory": str(fac.Code),
                        }
                    ]
                )

            percent = 0
            repercent = 0
            if chk > 0:
                percent = (cases / chk) * 100
            if (chk + recases) > 0:
                repercent = (recases / (chk + recases)) * 100
            if percent == 100.0 and repercent <= 10 and chk >= 3:
                elig += 1
            else:
                nonelig += 1

            payload.extend(
                [
                    {"type": fac.Code, "value": cases, "caseType": "Qualified"},
                    {"type": fac.Code, "value": Discases, "caseType": "Unqualified"},
                ]
            )
            typeT.extend(
                [
                    {"type": fac.Code, "value": t0, "caseType": "T0"},
                    {"type": fac.Code, "value": t1, "caseType": "T1"},
                    {"type": fac.Code, "value": t2, "caseType": "T2"},
                    {"type": fac.Code, "value": t3, "caseType": "T3"},
                    {"type": fac.Code, "value": chk, "caseType": "All Cases"},
                ]
            )
        return Response(
            {
                "Cases": {
                    "Total": tot,
                    "New": new,
                    "Inprogress": pro,
                    "Resolved": res,
                    "Closed": cls,
                },
                "factory": {"Eligible": elig, "Ineligible": nonelig},
                "payload": payload,
                "typeT": typeT,
                "sevCases": {
                    "Low": low_percentage,
                    "Medium": medium_percentage,
                    "High": high_percentage,
                },
                "compCases": [
                    {"type": "Voice call", "value": ivr},
                    {"type": "In-person", "value": inper},
                    {"type": "Workers Committee", "value": wc},
                    {"type": "Suggestions Box", "value": sb},
                ],
                "UtilisationRate": utilisation_rate,
            }
        )



class CaseTrbListAV(generics.ListAPIView):
    serializer_class = BaseUserModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        c = self.kwargs['c']
        f = self.kwargs['f']
        userRoles=UserRoleFactory.objects.filter(role__role=UserRole.CASE_TROUBLESHOOTER,user_fk__company_fk=c,factory_fk=f,is_active=True)
        user_ids = userRoles.values('user_fk_id').distinct()

        return BaseUserModel.objects.filter(id__in=user_ids)

class CaseManListAV(generics.ListAPIView):
    serializer_class = BaseUserModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        c = self.kwargs['c']
        f = self.kwargs['f']
        userRoles=UserRoleFactory.objects.filter(role__role=UserRole.CASE_MANAGER,user_fk__company_fk=c,factory_fk=f,is_active=True)
        user_ids = userRoles.values('user_fk_id').distinct()
        return BaseUserModel.objects.filter(id__in=user_ids)


class CCReportDetailsAV(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CaseReportSerializers

    def get_queryset(self):
        case = self.kwargs['pk']

        return CaseReslovingReport.objects.filter(Case=case)


class FactoryDetailsAV(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Factory.objects.all()
    serializer_class = FactorySerializer


# class CaseRepDetailsAV(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = BaseUserModel.objects.filter(role=UserRole.CASE_REPORTER)
#     serializer_class = BaseUserModelSerializer


# class CaseManDetailsAV(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = BaseUserModel.objects.filter(role=UserRole.CASE_MANAGER)
#     serializer_class = BaseUserModelSerializer


# class CaseTrbDetailsAV(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = BaseUserModel.objects.filter(role=UserRole.CASE_TROUBLESHOOTER)
#     serializer_class = BaseUserModelSerializer





# class CaseDetailsWithFile(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Case.objects.all()
#     serializer_class = CaseFileUploadSerializer


class CaseCountView(APIView):
    def get(self, request: Request) -> Response:
        ct_count = Case.objects.all().count()
        return Response({"Count": ct_count})




class ReportIncntvView(APIView):
    def get(self, request: Request) -> Response:
        data = request.data
        startDate = data['from']
        endDate = data['to']
        factory = data['Factory']

        try:
            case = Case.objects.filter(
                Date__range=[startDate, endDate], Factory=factory)
        except case.count() < 1:
            return Response({'Error': "No cases"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CaseSerializers(case, many=True)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class WinnerView(APIView):
    def get(self, request: Request) -> Response:
        data = request.data
        company = data['Company']
        res = []
        awrnpgms = 0
        # global T1d
        # T1d=0

        # variable=0
        factory = Factory.objects.filter(Company=company)
        for fac in factory.iterator():
            T0 = 0
            T1 = 0
            cases = Case.objects.filter(Factory=fac.id)
            for case in cases.iterator():
                if case.T0 == 1:
                    T0 = T0 + 1
                if case.T1 == 1:
                    T1 = T1 + 1
            if T0 == cases.count() and T1 == cases.count():
                variable = 1
            else:
                variable = 0
                # return Response({'Error':"No cases"},status=status.HTTP_404_NOT_FOUND )
            if fac.AwrnsPgms >= 2:
                awrnpgms = 1
            else:
                awrnpgms = 0
            if fac.ClosedCases >= 3:
                cc = 1
            else:
                cc = 0
            if variable == 1 and awrnpgms == 1 and cc == 1:
                # print(variable)
                res.append(fac.id)
        # sdata=FactorySerializer(res,many=True)
        # if (res.__len__()>1):
        #     fnl=res.ClosedCases.sort()
        #     print(fnl[-1])

        # else:
        # data=json.dumps(sdata)
        return Response(json.dumps(res))


@transaction.atomic
@csrf_exempt
def CaseCallwebhook(request:Request)->HttpResponse:
    if request.method == 'POST':
        token = environ.get('TATA_TOKEN')
        if request.headers.get('Tatata') != token:
            return HttpResponseForbidden(
                "Incorrect token in Acme-Webhook-Token header.",
                content_type="text/plain",
            )
        # approach1
        # Check whether there is an active case registered for a complainer
        # If yes
        # Then check how many active cases are against this number and add this rec to the active cases logs
        # If no
        # Create new case

        #    approach 2
        # extract data from body
        # parse it
        # check if the call is re. new case or and existing one
        # if eexisting case
        # add it into the log of the case
        # if new case
        # make a new case wothin that factory
        # assign  cr to it
        payload = json.loads(request.body)
        TatawebhooksLog.objects.create(
            receivedAt=timezone.now(),
            payload=payload,
        )
        try:
            language = payload["call_flow"][3]["name"].split("+")[0]
        except:
            language=Language.English
        factory = Factory.objects.get(Number=payload['call_to_number'])
        try:
            comp = Complainer.objects.get(PhoneNo=payload['caller_id_number'])#, Company=factory.Company,
                                          #Factory=factory)
            comp.is_active = True
            comp.Company=factory.Company
            comp.Factory=factory
            comp.Language=language
            comp.save()
        except Complainer.DoesNotExist:
            # if Complainer.objects.filter(PhoneNo=payload["caller_id_number"],Company=factory.Company).exists():
            #     print(
            #         "Cannot register your Case, you are calling at different factory number"
            #      )
            #     return HttpResponse(
            #         "Cannot register your Case, you are calling at different factory number"
            #     )
            # elif Complainer.objects.filter(PhoneNo=payload["caller_id_number"]).exists():
            #     print(
            #         "Cannot register your Case, you are calling at different company number"
            #     )  
            #     return HttpResponse(
            #         "Cannot register your Case, you are calling at different company number"
            #     )
            company = factory.Company

            comp = Complainer.objects.create(
                PhoneNo=payload["caller_id_number"], Company=company, Factory=factory, Language = language
            )

        case = Case.objects.filter(Complainer=comp,Company=factory.Company, Factory=factory).exclude(
            Q(CaseStatus=CaseStatus.CLOSED) | Q(CaseStatus=CaseStatus.UNRESPONSIVE)
        )
        if case.exists():
            for case in case.iterator():
                caseFreeze = Incentives.objects.get(Case=case)
                if case.CaseStatus == CaseStatus.ASSIGNED_TO_REPORTER:
                    if (caseFreeze.CRsendDate is not None) and (caseFreeze.CRreceiveDate is None):
                        caseFreeze.CRreceiveDate = current_time()
                elif case.CaseStatus == CaseStatus.ASSIGNED_TO_MANAGER:
                    if (caseFreeze.CMsendDate is not None) and (caseFreeze.CMreceiveDate is None):
                        caseFreeze.CMreceiveDate = current_time()
                elif (case.CaseStatus in [CaseStatus.ASSIGNED_TO_TROUBLESHOOTER, CaseStatus.UNDER_INVESTIGATION, CaseStatus.RE_INVESTIGATION]):
                    if (caseFreeze.CTsendDate is not None) and (caseFreeze.CTreceiveDate is None):
                        caseFreeze.CTreceiveDate = current_time() 
                tasks = scheduleInformation.objects.filter(type=scheduleType.SEND_MESSAGE)
                for task in tasks:
                    if task.Information["Case"] == case.id and task.is_active == True:
                        task.is_active = False
                        task.save()
                caseFreeze.save()
                print("wefed: ",UserRoleFactory.objects.get(role__role=UserRole.DEFAULT_ROLE),)
                auditlog = AuditLog.objects.create(
                    case=case,
                    status=case.CaseStatus,
                    created_by=UserRoleFactory.objects.get(role__role=UserRole.DEFAULT_ROLE),
                    # var_changed="Case Call recieved",
                    prev_state=str(case),
                    current_state=str(case),
                    message=payload["recording_url"],
                    action_type="Revert Message from the Worker - POST",
                )
            return HttpResponse("Logs added to case")

        else:
            if is_silent(payload["recording_url"]):
                blankcase = Case.objects.create(
                    Company=comp.Company,
                    Factory=comp.Factory,
                    ReportingMedium="Call",
                    CaseStatus=CaseStatus.CLOSED,
                    Complainer=comp,
                    CallRecording_url=payload["recording_url"],
                    CaseNature=CaseNature.COMPLAIN,
                    CaseValidation = False,
                    CaseCategory = "Invalid",
                )
                company = Company.objects.get(id=blankcase.Company.id)
                factory = Factory.objects.get(id=blankcase.Factory.id)
                casenumber = (
                        ConstantVars.INACHE + factory.region.Name[0] + factory.Code + str(blankcase.id)
                )
                blankcase.CaseNumber = casenumber
                blankcase.save()
                auditlog = AuditLog.objects.create(
                    case=blankcase,
                    status=blankcase.CaseStatus,
                    created_by=UserRoleFactory.objects.get(role__role=UserRole.DEFAULT_ROLE),
                    prev_state=str(blankcase),
                    current_state=str(blankcase),
                    message=payload["recording_url"],
                    action_type=ActionTypes.CASE_CLOSED
                )
                body = sendCategoryMessage(blankcase,"unClear Message")
                acklog = AuditLog.objects.create(
                    case=blankcase,
                    status=blankcase.CaseStatus,
                    created_by=UserRoleFactory.objects.get(role__role=UserRole.DEFAULT_ROLE),
                    prev_state=str(blankcase),
                    current_state=str(blankcase),
                    message=body,
                    action_type=ActionTypes.UNCLEAR_MESSAGE_SENT,
                )
            else:
                newcase = Case.objects.create(
                    Company=comp.Company,
                    Factory=comp.Factory,
                    ReportingMedium="Call",
                    CaseStatus=CaseStatus.ASSIGNED_TO_REPORTER,
                    Complainer=comp,
                    CallRecording_url=payload["recording_url"],
                    CaseNature=CaseNature.COMPLAIN,
                    T1vrfDate = current_time()
                )
                company = Company.objects.get(id=newcase.Company.id)
                factory = Factory.objects.get(id=newcase.Factory.id)
                casenumber = (
                        ConstantVars.INACHE + factory.region.Name[0] + factory.Code + str(newcase.id)
                )
                newcase.CaseNumber = casenumber
                newcase.save()
                auditlog = AuditLog.objects.create(
                    case=newcase,
                    status=newcase.CaseStatus,
                    created_by=UserRoleFactory.objects.get(role__role=UserRole.DEFAULT_ROLE),
                    # var_changed="Case Upload",
                    prev_state=str(newcase),
                    current_state=str(newcase),
                    message=payload["recording_url"],
                    action_type="Case Uploaded - POST",
                )

                cr = assigncR(casenumber)
                newcase.CaseReporter = cr
                newcase.save()
                body = sendCategoryMessage(newcase,"Registration Message")

                # caselog = CaseLogs.objects.create(
                #     Case=newcase,
                #     Message=body,
                #     Rec_URL=payload["recording_url"],
                #     CaseStatus=newcase.CaseStatus,
                #     cr_datetime=current_time(),
                # )
                acklog = AuditLog.objects.create(
                    case=newcase,
                    status=newcase.CaseStatus,
                    created_by=UserRoleFactory.objects.get(role__role=UserRole.DEFAULT_ROLE),
                    prev_state=str(newcase),
                    current_state=str(newcase),
                    message=body,
                    action_type=ActionTypes.CASE_ACK_MESSAGE_SENT,
                )

            return HttpResponse("Webhook received!")

def is_silent(mp3_url):

    # Disable SSL certificate verification
    ssl._create_default_https_context = ssl._create_unverified_context

    # Extract the filename from the URL
    mp3_filename = mp3_url.split("/")[-1]

    # Download the MP3 file from the URL
    urllib.request.urlretrieve(mp3_url, mp3_filename)

    # Convert the MP3 file to WAV format
    audio = AudioSegment.from_mp3(mp3_filename)
    wav_filename = mp3_filename.replace(".mp3", ".wav")
    audio.export(wav_filename, format="wav")

    # # Get the absolute path of the WAV file
    # wav_path = os.path.abspath(wav_filename)

    # Load the converted WAV file
    with sr.AudioFile(wav_filename) as audio_file:
        recognizer = sr.Recognizer()
        audio_data = recognizer.record(audio_file)

    os.remove(mp3_filename)
    os.remove(wav_filename)

    # duration = len(audio_data) / audio_data.sample_rate
    # #duration = audio_data.duration_seconds
    # #duration = audio_data.duration

    # if duration <= 15:
    #     try:
    #         text = recognizer.recognize_google(audio_data)

    #         if not text:
    #             # no audio - silent - return True
    #             return True
    #         else:
    #             # audio is there - not silent - return False
    #             return False
    #     except UnknownValueError:
    #         #if no text i.e, no audio - then error comes, so it is silent - return True
    #         return True
    # else:
    #     # return False if more than 15 seconds irrespective of sound is present or not
    #     return False

    try:
        text = recognizer.recognize_google(audio_data)
        # if text - voice detected - is_silent is False
        if text:
            return False
        # if no text - no voice - is_silent is True
        else:
            return True
    # if no text recognised error - no voice - is_silent is True
    except UnknownValueError:
        return True


def sendCategoryMessage(case,category):
    try:
        template = SMSTemplates.objects.get(Company=case.Company,template_categories__contains=[category],language=case.Complainer.Language)
    except:
        template = SMSTemplates.objects.get(Company=case.Company,template_categories__contains=[category],language=Language.English)
    templateID = template.templateID
    body = template.body
    matches = re.findall(r"\&@{(.+?)}",body)
    for match in matches:
        words = match.split(".")
        try:
            model = apps.get_model(app_label="accounts", model_name=words[0])
            if words[0] == "Case":
                value = model.objects.get(id=case.id).__getattribute__(words[1])
            elif words[0] == "Factory":
                value = model.objects.get(id=case.Factory.id).__getattribute__(words[1])
            else:
                continue
            body = re.sub(fr"\&@{{{match}\}}", str(value), body)
        except:
            continue
    code = sendcasemessage(templateID,body,str(case.Complainer.PhoneNo),case.Company)
    return body

def unResponsiveMessage(case,details):
    matches = re.findall(r"\&@{(.+?)}",details)
    for match in matches:
        words = match.split(".")
        try:
            model = apps.get_model(app_label="accounts", model_name=words[0])
            if words[0] == "Case":
                value = model.objects.get(id=case.id).__getattribute__(words[1])
            elif words[0] == "Factory":
                value = model.objects.get(id=case.Factory.id).__getattribute__(words[1])
            else:
                continue
            details = re.sub(fr"\&@{{{match}\}}", str(value), details)
        except:
            continue
    return details


#sending closing message by fetching details from resolution message
def caseClosingMessage(case):
    report = CaseReslovingReport.objects.get(Case=case)
    language = report.CCLanguage
    # get the closing template based on resolution template language
    template = SMSTemplates.objects.get(Company=case.Company,template_categories__contains=['Closing Message'],language=language)
    templateID = template.templateID
    body = template.body
    # autofill template with things like factory number and case number
    matches = re.findall(r"\&@{(.+?)}",body)
    for match in matches:
        words = match.split(".")
        try:
            model = apps.get_model(app_label="accounts", model_name=words[0])
            if words[0] == "Case":
                value = model.objects.get(id=case.id).__getattribute__(words[1])
            elif words[0] == "Factory":
                value = model.objects.get(id=case.Factory.id).__getattribute__(words[1])
            else:
                continue
            body = re.sub(fr"\&@{{{match}\}}", str(value), body)
        except:
            continue
    # getting user given values from resolution message, translating them and filling the closing template
    matches = re.findall(r"\${(.+?)}",body)
    variables = json.loads(report.CCRvariables)
    key = {"Hindi":"hi","Kannada":'kn',"Punjabi":'pa'}
    for match in matches:
        try:
            if language == "English":
                value = variables[match]
            else:
                value = translate_text(variables[match],'en',key[language])
            body = re.sub(fr"\${{{match}\}}", str(value), body)
        except:
            continue
    #sending the closing message to the complainer
    code = sendcasemessage(templateID,body,str(case.Complainer.PhoneNo),case.Company)
    return body

class CaseSendMessageKlyra(APIView):
    # permission_classes = [HasGroupPermission]
    # required_groups = {
    #     'POST': ['CR','CM','CT','FACTORY_ADMIN','SUPER_ADMIN'],
    # }
    # model = "case"

    def post(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        data = request.data
        case = Case.objects.get(id=request.data['Case'])
        temp = data["templateID"]
        role = data["userRole"]
        body = data["message"]
        company = data["Company"]
        errorResponse={"error":" User is not allowed to send a message at this stage"}
        user_allow_bool=send_message_user_validation(case,request)
        if user_allow_bool==False:
            return Response(errorResponse,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        T2vrfDate = localtime(case.T2vrfDate)
        # T2 will be calculated only if it is ct and only if he sends one of the three acknowledgement messages to worker
        template = SMSTemplates.objects.get(templateID=temp,Company=company)
        caseFreeze = Incentives.objects.get(Case=case)
        if ("Acknowledgement Message" in template.template_categories):
            if (role == UserRole.CASE_TROUBLESHOOTER) and (case.CaseStatus != CaseStatus.UNDER_INVESTIGATION):
                # not allowing user to go to next phase without him getting worker reply if asked 
                if (caseFreeze.CTsendDate is not None) and (caseFreeze.CTreceiveDate is None):
                    return Response("Wait for worker's reply before pushing case to next stage") 
                case.Counter = 4
                case.CaseStatus = CaseStatus.UNDER_INVESTIGATION
                startDate = T2vrfDate
                endDate = current_time()
                days = working_days(startDate, endDate,case.Factory)
                case.T3vrfDate = endDate
                if days <= 1:
                    case.T2 = 1
                    case.T2Breached = False
                else:
                    case.T2 = days
                    case.T2Breached = True
                case.save()
                auditlog = AuditLog.objects.create(
                case=case,
                status=case.CaseStatus,
                created_by=userRole,
                prev_state="",
                current_state="",
                message=body,
                action_type=ActionTypes.CT_FIRST_RESPONSE_SENT,
                )
            elif (role == UserRole.REGIONAL_ADMIN) and (case.CaseStatus != CaseStatus.RA_INVESTIGATION):
                case.CaseStatus = CaseStatus.RA_INVESTIGATION
                case.T3vrfDate = current_time()
                case.save()
                auditlog = AuditLog.objects.create(
                case=case,
                status=case.CaseStatus,
                created_by=userRole,
                prev_state="",
                current_state="",
                message=body,
                action_type=ActionTypes.RA_FIRST_RESPONSE_SENT,
                )

        elif ("Requirement Message" in template.template_categories):
            if (role != UserRole.REGIONAL_ADMIN):
                def jobCreate():
                    info = scheduleInformation.objects.create(
                        Information={
                            "templateID":template.templateID,
                            "body":body,
                            "PhoneNo":str(case.Complainer.PhoneNo),
                            "Company":case.Company.id,
                            "Case":case.id
                            },
                        type = scheduleType.SEND_MESSAGE
                    )
                caseFreeze = Incentives.objects.get(Case=case)
                if (role == UserRole.CASE_REPORTER):
                    if not caseFreeze.CRsendDate:
                        caseFreeze.CRsendDate = current_time()
                        jobCreate()
                elif (role == UserRole.CASE_MANAGER):
                    if not caseFreeze.CMsendDate:
                        caseFreeze.CMsendDate = current_time()
                        jobCreate()
                elif (role == UserRole.CASE_TROUBLESHOOTER):
                    if not caseFreeze.CTsendDate:
                        caseFreeze.CTsendDate = current_time()
                        jobCreate()
                caseFreeze.save()

                auditlog = AuditLog.objects.create(
                    case=case,
                    status=case.CaseStatus,
                    created_by=userRole,
                    prev_state="",
                    current_state="",
                    message=body,
                    action_type=ActionTypes.CASE_MESSAGE_SENT_REPLY_REQUIRED
,
                )
            elif (role == UserRole.REGIONAL_ADMIN):
                if case.CaseCategory == "POSH": 
                    auditlog = AuditLog.objects.create(
                    case=case,
                    status=case.CaseStatus,
                    created_by=userRole,
                    prev_state="",
                    current_state="",
                    message=body,
                    action_type=ActionTypes.FOLLOWUP_MESSAGE_POSH_SENT_WRITTEN_COMPLAINT_RA,
                )
                else:
                    auditlog = AuditLog.objects.create(
                        case=case,
                        status=case.CaseStatus,
                        created_by=userRole,
                        prev_state="",
                        current_state="",
                        message=body,
                        action_type=ActionTypes.FOLLOWUP_MESSAGE_SENT,
                    )

        else:
            auditlog = AuditLog.objects.create(
            case=case,
            status=case.CaseStatus,
            created_by=userRole,
            prev_state="",
            current_state="",
            message=body,
            action_type=" Case Message Sent - POST",
        )

        # try:
        #     template=SMSTemplates.objects.get(templateID=request.data["templateID"])
        # except MultipleObjectsReturned:
        #     template=SMSTemplates.objects.filter(templateID=request.data["templateID"]).first()
        '''comp=Company.objects.get(id=request.data["Company"])
        query = SMSTemplates.objects.filter(templateID=request.data["templateID"])
        template=query.get(Company=comp)'''
        # caselog = CaseLogs.objects.create(Case=case, Message=body)


        code = sendcasemessage(
            template.templateID, body, str(case.Complainer.PhoneNo), case.Company
        )
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        user_id = userRole.id
        cache_key = f'user_data_{user_id}_first'
        cache.delete(cache_key)
        message = {
            "message": "{} has been Sent successfully".format(
                template.Title
            ),
            "message_body": {"templateID":template.templateID,"Title":template.Title,"body":body,"language":template.language},
        }
        return Response(message, status=status.HTTP_200_OK)


def assigncR(casenumber:str)->UserRoleFactory:
    try:
        case = Case.objects.get(CaseNumber=casenumber)
    except Case.MultipleObjectsReturned:
        return False
    data = {}
    # cr = BaseUserModel.objects.filter(
    #     company_fk=case.Company, factory_fk=case.Factory,role=UserRole.CASE_REPORTER,is_active=True)
    cr = UserRoleFactory.objects.filter(user_fk__company_fk=case.Company,factory_fk=case.Factory,role__role=UserRole.CASE_REPORTER,is_active=True)
    if cr.count() == 1:
        case.CaseReporter = cr[0]
        case.save()
        return cr[0]
    elif (cr.count() == 0):
        return "not assigned"
    for item in cr:
        cs = Case.objects.filter(CaseReporter=item)
        data[item] = cs.count()
    # finding minimum case nums from crs
    # returns the original list if all the equal
    temp = min(data.values())
    res = [key for key in data if data[key] == temp]
    if (len(res) > 1):
        ran = random.choice(res)
        case.CaseReporter = ran
        case.save()
        return ran
    elif (len(res) == 1):
        case.CaseReporter = res[0]
        case.save()
        return res[0]
    # return "done"

class RequestPasswordResetEmailAV(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailSerializer

    def post(self, request: Request) -> Response:
        email = request.data['email']
        if BaseUserModel.objects.filter(email=email).exists():
            serializer = self.serializer_class(
                data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                return Response({'success': 'We have sent you a link to reset your password'},
                                status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'Email is invalid'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAV(generics.GenericAPIView):
    def get(self, request:Request, uidb64, token:str)->Response:
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = BaseUserModel.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid token,TimeOut Please Request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:

            return Response({'error': 'Invalid token,TimeOut Please Request a new one'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAV(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': "True", 'message': "Password Changed Successfully"}, status=status.HTTP_200_OK)


fss = FileSystemStorage(location="templates/")


@api_view(['POST', 'PUT'])
def importtemplate(request:Request)->Response:
    file = request.FILES['file']
    content = file.read()
    file_content = ContentFile(content)
    file_name = fss.save(
        "temp.csv", file_content
    )
    tmp_file = fss.path(file_name)
    csv_file = open(tmp_file, errors="ignore")
    reader = csv.reader(csv_file)
    next(reader)

    product_list = []
    for id_, row in enumerate(reader):
        (Title, Language, TempId, body, company, template_categories, user_roles_access, variables) = row
        #print(type(json.loads(row[7])))
        #matches = re.findall(r"\${(.+?)}", row[2])
        #words = row[0].split("/")
        number = int(row[4])
        product_list.append(
            SMSTemplates(
                Title=row[0],
                templateID=row[2],
                body=row[3],
                language=row[1],
                variables=row[7],
                Company=Company.objects.get(id=number),
                template_categories=row[5],
                user_roles_access=row[6],
            )
        )

    SMSTemplates.objects.bulk_create(product_list)

    return Response("Successfully upload the data")


# fss = FileSystemStorage(location="masterdata/")



fss = FileSystemStorage(location="departments/")

@api_view(["POST"])
def DepartmentUpload(request:Request)->Response:
    file = request.FILES["file"]
    content = file.read()
    file_content = ContentFile(content)
    file_name = fss.save("departments.csv", file_content)
    tmp_file = fss.path(file_name)
    csv_file = open(tmp_file, errors="ignore")
    reader = csv.reader(csv_file)
    next(reader)

    dept_list = []
    for id_, row in enumerate(reader):
        (Unit, Department, SubDepartment) = row
        dept_list.append(
            FactoryDepartment(
                factory=Factory.objects.get(Code=Unit),
                Department=Department,
                SubDepartment=SubDepartment,
            )
        )

    FactoryDepartment.objects.bulk_create(dept_list)


    return Response("Successfully upload the data")


class GetSmstemplates(APIView):
    def post(self, request: Request) -> Response:
        try:
            temp = SMSTemplates.objects.get(templateID=request.data["templateID"])
        except SMSTemplates.DoesNotExist:
            return Response(
                {"Error": "Template Not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = SMSTemplatesSerializer(temp)
        return Response(serializer.data)



def sorting(replogs, manlogs, trblogs, ralogs, unreslogs:dict or QuerySet)->dict:
    length = len(replogs)
    response = replogs
    if manlogs is not None:
        for key in manlogs:
            response[length] = manlogs[key]
            length = length + 1
    length = len(response)
    if trblogs is not None:
        for key in trblogs:
            response[length] = trblogs[key]
            length = length + 1
    length = len(response)
    if ralogs is not None:
        for key in ralogs:
            response[length] = ralogs[key]
            length = length + 1
    length = len(response)
    if unreslogs is None:
        return response
    else:
        for key in unreslogs:
            response[length] = unreslogs[key]
            length = length + 1

    # print((response))
    return response


class ViewLogsAV(APIView):
    def get(self, request: Request) -> Response:
        case = Case.objects.get(id=request.GET.get("case"))
        auditlogs = AuditLog.objects.filter(case=case)
        # print(auditlogs)
        replogs = ASSIGNED_TO_REPORTER(auditlogs)
        manlogs = ASSIGNED_TO_MANAGER(auditlogs)
        trblogs = ASSIGNED_TO_TRB(auditlogs)
        ralogs = ASSIGNED_TO_RA(auditlogs)
        unreslogs = UNRESPONSIVE(auditlogs)
        response = sorting(replogs, manlogs, trblogs, ralogs, unreslogs)
        sorted_dict = dict(sorted(response.items(), key=lambda x: x[1]['timestamp']))

        return Response(sorted_dict)


def ackmessage(acklog, caseuploadlog):
    if caseuploadlog.case.ReportingMedium == ReportingMedium.CALL and acklog!="":
        response = {
            "identifier": ViewLogsIdentifier.ACKMSG,
            "title": "Acknowledgement Message Sent & Case Reporter Assigned",
            "timestamp": caseuploadlog.created_at,
            "recording_url": caseuploadlog.message,
            "message": acklog.message,
            "medium": caseuploadlog.case.ReportingMedium,
        }
        
    elif((caseuploadlog.case.ReportingMedium == ReportingMedium.IN_PERSON
        or caseuploadlog.case.ReportingMedium == ReportingMedium.WORKER_COMMITTEE) and caseuploadlog.case.Complainer ):
        response = {
            "identifier": ViewLogsIdentifier.ACKMSG,
            "title": "Acknowledgement Message Sent & Case Reporter Assigned",
            "timestamp": caseuploadlog.created_at,
            "recording_url": caseuploadlog.message,
            "message": acklog.message,
            "medium": caseuploadlog.case.ReportingMedium,
        }
    elif (
        (caseuploadlog.case.ReportingMedium == ReportingMedium.IN_PERSON
        or caseuploadlog.case.ReportingMedium == ReportingMedium.WORKER_COMMITTEE) and caseuploadlog.case.Complainer is None
    ):
        response = {
            "identifier": ViewLogsIdentifier.ACKMSG,
            "title": "Case Reporter Assigned",
            "timestamp": caseuploadlog.created_at,
            "medium": caseuploadlog.case.ReportingMedium,
        }
    elif (
        caseuploadlog.case.ReportingMedium == ReportingMedium.SUGGESTION_BOX
       
    ):
        response = {
            "identifier": ViewLogsIdentifier.ACKMSG,
            "title": "Case Reporter Assigned",
            "timestamp": caseuploadlog.created_at,
            "medium": caseuploadlog.case.ReportingMedium,
        }

    return response

def Invalidation(caseInvalidate):
    response = {
        "identifier": ViewLogsIdentifier.INVALIDATED,
        "title": "Case is Marked Invalid by Case Reporter",
        "timestamp": caseInvalidate.created_at,
    }

    return response

def closingMessage(case):
    response = {
        "identifier": ViewLogsIdentifier.CLOSEMSG,
        "title": "Case Closing Message Sent",
        "timestamp": case.created_at,
        "message": case.message,
    }

    return response

def Unresponsive(case):
    response = {
        "identifier": ViewLogsIdentifier.STATECHNG,
        "title": "Case Closed due to lack of response from the worker",
        "timestamp": case.created_at,
    }

    return response

def unResponsiveSent(case):
    response = {
        "identifier": ViewLogsIdentifier.CLOSEMSG,
        "title": "Case Close Due to Lack of Response, Message sent",
        "timestamp": case.created_at,
        "message": case.message,
    }

    return response


def sentmessage(logs,count):
    response = {}
    i = 0

    # print((logs), count)
    if count > 1:
        for log in logs:
            # print(log, "svhjv")
            res = {
                "identifier": ViewLogsIdentifier.SENTMSG,
                "title": "Message sent by " + log.created_by.role.role,
                "timestamp": log.created_at,
                "message": log.message,
            }
            response[i] = res
            i = i + 1
    elif count == 0:
        return None
    elif count == 1 and isinstance(logs, QuerySet) == True:
        res = {
            "identifier": ViewLogsIdentifier.SENTMSG,
            "title": "Message sent by " + logs[0].created_by.role.role,
            "timestamp": logs[0].created_at,
            "message": logs[0].message,
        }
        response[0] = res
    elif count == 1 and isinstance(logs, AuditLog) == True:
        res = {
            "identifier": ViewLogsIdentifier.SENTMSG,
            "title": "Message sent by " + logs.created_by.role.role,
            "timestamp": logs.created_at,
            "message": logs.message,
        }
        response[0] = res

    return response
# make sure posh message requirement followup is being accounted over here.
def followmessage(logs): 
    response = {}
    number = 1
    i = 0
    
    for log in logs:
        res = {
                "identifier": ViewLogsIdentifier.SENTMSG,
                "title": "Follow-up Message Sent - " + str(number),
                "timestamp": log.created_at,
                "message": log.message,
            }
        response[i] = res
        i = i + 1
        number = number + 1

    return response




def revertmessage(logs, count):
    response = {}
    i = 0

    # print((logs), count)
    if count > 1:
        for log in logs:
            # print(log, "svhjv")
            if(log.status=="Resolved"):
                res = {
                "identifier": ViewLogsIdentifier.REVERTMSG,
                "title": "Feedback Message from the Worker",
                "timestamp": log.created_at,
                "recording_url": log.message,
            }
            else:
                res = {
                "identifier": ViewLogsIdentifier.REVERTMSG,
                "title": "Revert Message from the Worker",
                "timestamp": log.created_at,
                "recording_url": log.message,
                }
            response[i] = res
            i = i + 1
    elif count == 0:
        return None
    elif count == 1 and isinstance(logs, QuerySet) == True:
        res = {
            "identifier": ViewLogsIdentifier.REVERTMSG,
            "title": "Revert Message from the Worker",
            "timestamp": logs[0].created_at,
            "recording_url": logs[0].message,
        }
        response[0] = res
    elif count == 1 and isinstance(logs, AuditLog) == True:
        res = {
            "identifier": ViewLogsIdentifier.REVERTMSG,
            "title": "Revert Message from the Worker",
            "timestamp": logs.created_at,
            "recording_url": logs.message,
        }
        response[0] = res

    return response


def statechange(logs,count):
    response = {}
    i = 0

    # print((logs), count)
    if count > 1:
        for log in logs:
            res={}
            split = log.action_type.split(" - ")
            if(log.action_type=="CaseStatus Updated - PUT" and log.current_state==CaseStatus.UNDER_INVESTIGATION):
                # print(log, "svhjv")
                res = {
                    "identifier": ViewLogsIdentifier.STATECHNG,
                    "title": "Case is Under Investigation now",
                    "timestamp": log.created_at,
                }

            elif(log.action_type=="CaseStatus Updated - PUT" and log.current_state==CaseStatus.RA_INVESTIGATION):
                # print(log, "svhjv")
                res = {
                    "identifier": ViewLogsIdentifier.STATECHNG,
                    "title": "Case is being Investigated under Regional Admin now",
                    "timestamp": log.created_at,
                }
                
            elif(log.action_type=="CaseStatus Updated - PUT" and log.current_state==CaseStatus.RE_INVESTIGATION):
                # print(log, "svhjv")
                res = {
                    "identifier": ViewLogsIdentifier.STATECHNG,
                    "title": "Case is under Re-Investigation",
                    "timestamp": log.created_at,
                }

            elif(log.action_type=="CaseStatus Updated - PUT" and log.current_state==CaseStatus.RE_INVESTIGATION_RA):
                # print(log, "svhjv")
                res = {
                    "identifier": ViewLogsIdentifier.STATECHNG,
                    "title": "Case is under Regional Admin Re-Investigation",
                    "timestamp": log.created_at,
                }
                # print(res)
            elif (split[0]=="Case Resolved by CT") or (split[0]=="Case Resolved by RA"):
                if Case.objects.get(id=logs[0].case_id).Complainer is not None:                        
                    res = {
                        "identifier": ViewLogsIdentifier.STATECHNG,
                        "title": split[0]+" & Resolution Message Sent",
                        "timestamp": log.created_at,
                    }
                else:
                    res = {
                        "identifier": ViewLogsIdentifier.STATECHNG,
                        "title": split[0],
                        "timestamp": log.created_at,
                    }
            else:
                # print(split[0])
                res = {
                    "identifier": ViewLogsIdentifier.STATECHNG,
                    "title": split[0],
                    "timestamp": log.created_at,
                }
            response[i] = res
            i = i + 1
    elif count == 0:
        return None
    elif count == 1 and isinstance(logs, QuerySet) == True:
        split = logs[0].action_type.split(" - ")
        # print(split,"query")
        if (split[0]=="Case Resolved by CT") or (split[0]=="Case Resolved by RA"):
                if Case.objects.get(id=logs[0].case_id).Complainer is not None:
                        res = {
                        "identifier": ViewLogsIdentifier.STATECHNG,
                        "title": split[0]+" & Resolution Message Sent",
                        "timestamp": logs[0].created_at,
                    }
                else:
                    res = {
                        "identifier": ViewLogsIdentifier.STATECHNG,
                        "title": split[0],
                        "timestamp": logs[0].created_at,
                    }
        elif(logs[0].action_type=="CaseStatus Updated - PUT" and logs[0].current_state==CaseStatus.UNDER_INVESTIGATION):
                res = {
                    "identifier": ViewLogsIdentifier.STATECHNG,
                    "title": "Case is Under Investigation now",
                    "timestamp": logs[0].created_at,
                }

        elif(logs[0].action_type=="CaseStatus Updated - PUT" and logs[0].current_state==CaseStatus.RA_INVESTIGATION):
                res = {
                    "identifier": ViewLogsIdentifier.STATECHNG,
                    "title": "Case is being Investigated under Regional Admin now",
                    "timestamp": logs[0].created_at,
                }

        elif(logs[0].action_type=="CaseStatus Updated - PUT" and logs[0].current_state==CaseStatus.RE_INVESTIGATION):
                # print(log, "svhjv")
                res = {
                    "identifier": ViewLogsIdentifier.STATECHNG,
                    "title": "Case is under Re-Investigation",
                    "timestamp": logs[0].created_at,
                }

        elif(logs[0].action_type=="CaseStatus Updated - PUT" and logs[0].current_state==CaseStatus.RE_INVESTIGATION_RA):
                # print(log, "svhjv")
                res = {
                    "identifier": ViewLogsIdentifier.STATECHNG,
                    "title": "Case is under Regional Admin Re-Investigation",
                    "timestamp": logs[0].created_at,
                }
        else:
                # print(split[0])

                res = {
                    "identifier": ViewLogsIdentifier.STATECHNG,
                    "title": split[0],
                    "timestamp": logs[0].created_at,
                }

        response[0] = res
    elif count == 1 and isinstance(logs, AuditLog) == True:
        split = logs.action_type.split(" - ")
        # print(split,"audit")

        if split[0]=="Case Resolved by CT":
            if Case.objects.get(id=logs[0].case_id).Complainer is not None:
                    res = {
                        "identifier": ViewLogsIdentifier.STATECHNG,
                        "title": split[0]+" & Resolution Message Sent",
                        "timestamp": logs.created_at,
                    }
            else:
                res = {
                        "identifier": ViewLogsIdentifier.STATECHNG,
                        "title": split[0],
                        "timestamp": logs.created_at,
                    }
        # elif(logs[0].action_type=="CaseStatus Updated - PUT" and logs[0].current_state==CaseStatus.RE_INVESTIGATION):
        #         # print(log, "svhjv")
        #         res = {
        #             "identifier": ViewLogsIdentifier.STATECHNG,
        #             "title": "Case is being Investigated again",
        #             "timestamp": logs[0].created_at,
        #         }
        else:

                res = {
                    "identifier": ViewLogsIdentifier.STATECHNG,
                    "title": split[0],
                    "timestamp": logs.created_at,
                }
                # print("adasdsadsa")
        response[0] = res
    return response

def varchange(logs):
    response = {}
    var = {}
    time = current_time()
    for log in logs:
        if(log.prev_state !="") and (log.current_state!="") and logs.filter(var_changed=log.var_changed).count()==1:
            arr = [log.prev_state, log.current_state]
            var[log.var_changed] = arr
            time = log.created_at
        elif((log.prev_state !="") or (log.current_state!="")) and logs.filter(var_changed=log.var_changed).count()!=1:
            firstchng=logs.filter(var_changed=log.var_changed).first()
            lastchange=logs.filter(var_changed=log.var_changed).last()
            arr = [firstchng.prev_state, lastchange.current_state]
            var[log.var_changed] = arr
            time = lastchange.created_at
            
    # print(var)
    response = {
        "identifier": ViewLogsIdentifier.VARCHANGED,
        "title": "Changes made by Case Manager",
        "timestamp": time,
        "variables": var,
    }
    
    # print(logs)
    
    return response


def ASSIGNED_TO_REPORTER(auditlogs):
    fstset = auditlogs.filter(status__in=[CaseStatus.ASSIGNED_TO_REPORTER,CaseStatus.CLOSED])
    atrres = {}
    i = 0

    try:
        acklog = fstset.get(action_type__contains="Acknowledgement Message Sent")
        caseuploadlog = fstset.get(action_type__contains="Case Uploaded")
        ackres = ackmessage(acklog, caseuploadlog)
        atrres[0] = ackres
        i = i + 1

    except AuditLog.DoesNotExist:
        try:
            caseuploadlog = fstset.get(action_type__contains="Case Uploaded")
            ackres = ackmessage("", caseuploadlog)
            atrres[0] = ackres
            i = i + 1
        except:
            pass
    
    i = 1
    sentmsg = fstset.filter(action_type__contains="Case Message Sent")
    if sentmsg.count() != 0:
        responsesent = sentmessage(sentmsg, sentmsg.count())
        for key in responsesent:
            atrres[i] = responsesent[key]
            i = i + 1

    followmsg = fstset.filter(action_type__contains="Follow-up Message sent")
    if followmsg.count() != 0:
        msgsent = followmessage(followmsg)
        for key in msgsent:
            atrres[i] = msgsent[key]
            i = i + 1
        
    revertmsg = fstset.filter(action_type__contains="Revert Message")
    if revertmsg.count() != 0:
        responserev = revertmessage(revertmsg, revertmsg.count())

        for key in responserev:
            atrres[i] = responserev[key]
            i = i + 1

    check = fstset.filter(action_type__contains="Case is Marked Invalid by Case Reporter")
    if check.exists():
        caseInvalidate = check.first()
        invalidateResponse = Invalidation(caseInvalidate)
        atrres[i] = invalidateResponse
        i = i + 1

    caseclsd = fstset.filter(action_type__contains="Case Closed")
    if caseclsd.count()!=0:
        clsdres = statechange(caseclsd,caseclsd.count())
        for key in clsdres:
            atrres[i]=clsdres[key]
            i=i+1
    
    message = fstset.filter(action_type__contains="Unclear Message Sent")
    if message.exists():
        closeMessage = message.first()
        messageResponse = closingMessage(closeMessage)
        atrres[i] = messageResponse
        i = i + 1

    return atrres


def ASSIGNED_TO_MANAGER(auditlogs):
    secndset = auditlogs.filter(status__in=[CaseStatus.ASSIGNED_TO_MANAGER])
    try:
        trans2man = secndset.get(action_type__contains="Transferred to Case Manager")
    except AuditLog.DoesNotExist:
        return None
    response = statechange(trans2man,1)
    atmres = {}
    i=0
    atmres[i] = response[0]
    i=i+1
    varchngd = secndset.filter(
        var_changed__in=["Priority", "CaseNature", "CATEGORY", "SUBCATEGORY"]
    )
    if varchngd.count() != 0:
        varchangeres = varchange(varchngd)
        atmres[i] = varchangeres
        i=i+1
    else:
        pass
        # sentmsg

    sentmsg = secndset.filter(action_type__contains="Case Message Sent")
    if sentmsg.count() != 0:
        responsesent = sentmessage(sentmsg, sentmsg.count())
        for key in responsesent:
            atmres[i] = responsesent[key]
            i = i + 1
    # else:
    #     return atmres

    followmsg = secndset.filter(action_type__contains="Follow-up Message sent")
    if followmsg.count() != 0:
        msgsent = followmessage(followmsg)
        for key in msgsent:
            atmres[i] = msgsent[key]
            i = i + 1
        
    revertmsg = secndset.filter(action_type__contains="Revert Message")
    if revertmsg.count() != 0:
        revresponse = revertmessage(revertmsg, revertmsg.count())

        for key in revresponse:
            atmres[i] = revresponse[key]
            i = i + 1

    return atmres


def ASSIGNED_TO_TRB(auditlogs):
    thrdset = auditlogs.filter(
        status__in=[
            CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,
            CaseStatus.UNDER_INVESTIGATION,
            CaseStatus.RESOLVED,
            CaseStatus.RE_INVESTIGATION,
            CaseStatus.CLOSED,
        ]
    )
    try:
        trans2trb = thrdset.get(
            action_type__contains="Transferred to Case Troubleshooter"
        )
    except AuditLog.DoesNotExist:
        return None
    response = statechange(trans2trb,1)
    # print(response,"dsdsrb")
    attres = {}
    i=0
    attres[i] = response[0]
    i=i+1
    try:
        firstresponse_ct=thrdset.get(action_type__contains=" First Response Sent By CaseTroubleShooter - POST")
        firstres=statechange(firstresponse_ct,1)
        attres[i]=firstres[0]
        i=i+1
    except AuditLog.DoesNotExist:
        pass

    under_inves_stat=thrdset.filter(action_type__contains="CaseStatus Updated - PUT",current_state=CaseStatus.UNDER_INVESTIGATION)
    if under_inves_stat.count() != 0:
        userinvesres=statechange(under_inves_stat,under_inves_stat.count())
        for key in userinvesres:
            attres[i] = userinvesres[key]
            i = i + 1

    sentmsg = thrdset.filter(action_type__contains="Case Message Sent")
    # print(sentmsg,"dwewewewwewe")
    if sentmsg.count() != 0:
        responsesent = sentmessage(sentmsg, sentmsg.count())
        for key in responsesent:
            attres[i] = responsesent[key]
            i = i + 1
    # else:
    #     return attres
    # print(attres,"dasdsadsadsadasdsad")

    followmsg = thrdset.filter(action_type__contains="Follow-up Message sent")
    if followmsg.count() != 0:
        msgsent = followmessage(followmsg)
        for key in msgsent:
            attres[i] = msgsent[key]
            i = i + 1

    revertmsg = thrdset.filter(
        action_type__contains="Revert Message",
    )
    if revertmsg.count() != 0:
        revres = revertmessage(revertmsg, revertmsg.count())
        for key in revres:
            attres[i] = revres[key]
            i = i + 1
    else:
        pass

    caseresmsg = thrdset.filter(action_type__contains="Case Resolved by CT")
    if caseresmsg.count()!=0:
        responseresv = statechange(caseresmsg,caseresmsg.count())
        for key in responseresv:
            attres[i] = responseresv[key]
            i=i+1
    else:
        pass



    # try:
    #     caseresmsg = thrdset.get(action_type__contains="Case Resolved by CT")
    #     print(caseresmsg,"caseresolution")
    # except AuditLog.DoesNotExist:
    #     return attres
    # responseresv = statechange(caseresmsg)
    # attres[i] = responseresv
    # feedres = thrdset.filter(
    #         status=CaseStatus.RESOLVED, action_type__contains="Revert Message"
    #     )
    # if feedres.count()!=0:
    #     resfeed = revertmessage(feedres,feedres.count())
    #     for key in resfeed:
    #         attres[i] = resfeed[key]
    #         i=i+1
    # else:
    #     pass
    # try:
    #     feedres = thrdset.get(
    #         status=CaseStatus.RESOLVED, action_type__contains="Revert Message"
    #     )
    # except AuditLog.DoesNotExist:
    #     return attres

    # resfeed = revertmessage(feedres, 1)
    # attres[i + 1] = resfeed[0]
    caseclsd = thrdset.filter(action_type__contains="Case Closed")
    if caseclsd.count()!=0:
        clsdres = statechange(caseclsd,caseclsd.count())
        for key in clsdres:
            attres[i]=clsdres[key]
            i=i+1
    else:
        pass
    # try:
    #     caseclsd = thrdset.get(action_type__contains="Case Closed")
    # except AuditLog.DoesNotExist:
    #     return attres

    # # clsdres = statechange(caseclsd)
    # attres[i + 2] = clsdres
    casereopen=thrdset.filter(action_type__contains="Case Reopened ")
    if casereopen.count()!=0:
        reopencase_response=statechange(casereopen, casereopen.count())
        for key in reopencase_response:
            attres[i]=reopencase_response[key]
            i=i+1
    else :
        pass
    casere_investigation=thrdset.filter(action_type__contains="CaseStatus Updated - PUT",current_state=CaseStatus.RE_INVESTIGATION)
    if casere_investigation.count()!=0:
        reopencase_response=statechange(casere_investigation, casere_investigation.count())
        for key in reopencase_response:
            attres[i]=reopencase_response[key]
            i=i+1
    else :
        pass
    message = thrdset.filter(action_type__contains="Case Closing Message Sent")
    if message.exists():
        closeMessgae = message.first()
        messageResponse = closingMessage(closeMessgae)
        attres[i] = messageResponse
        i = i + 1
    else :
        pass
    # print(attres,"trbshooter")
    return attres

def ASSIGNED_TO_RA(auditlogs):
    frthset = auditlogs.filter(
        status__in=[
            CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN,
            CaseStatus.RA_INVESTIGATION,
            CaseStatus.RESOLVED,
            CaseStatus.RE_INVESTIGATION_RA,
            CaseStatus.CLOSED,
            CaseStatus.UNRESPONSIVE
        ]
    )
    try:
        trans2ra = frthset.get(
            action_type__contains=ActionTypes.RA_ASSIGNED
        )
    except AuditLog.DoesNotExist:
        return None
    response = statechange(trans2ra,1)
    # print(response,"dsdsrb")
    atares = {}
    i=0
    atares[i] = response[0]
    i=i+1
    try:
        firstresponse_ra=frthset.get(action_type__contains=ActionTypes.RA_FIRST_RESPONSE_SENT)
        firstres=statechange(firstresponse_ra,1)
        atares[i]=firstres[0]
        i=i+1
    except AuditLog.DoesNotExist:
        pass

    under_inves_stat=frthset.filter(action_type__contains=ActionTypes.STATUS_PUT,current_state=CaseStatus.RA_INVESTIGATION)
    if under_inves_stat.count() != 0:
        userinvesres=statechange(under_inves_stat,under_inves_stat.count())
        for key in userinvesres:
            atares[i] = userinvesres[key]
            i = i + 1

    sentmsg = frthset.filter(action_type__contains=ActionTypes.CASE_MESSAGE_SENT)
    if sentmsg.count() != 0:
        responsesent = sentmessage(sentmsg, sentmsg.count())
        for key in responsesent:
            atares[i] = responsesent[key]
            i = i + 1

    followmsg = frthset.filter(action_type__contains=ActionTypes.FOLLOWUP_MESSAGE_SENT)
    if followmsg.count() != 0:
        msgsent = followmessage(followmsg)
        for key in msgsent:
            atares[i] = msgsent[key]
            i = i + 1

    revertmsg = frthset.filter(
        action_type__contains=ActionTypes.REVERT_MESSAGE,
    )
    if revertmsg.count() != 0:
        revres = revertmessage(revertmsg, revertmsg.count())
        for key in revres:
            atares[i] = revres[key]
            i = i + 1
    else:
        pass

    caseresmsg = frthset.filter(action_type__contains="Case Resolved by RA")
    if caseresmsg.count()!=0:
        responseresv = statechange(caseresmsg,caseresmsg.count())
        for key in responseresv:
            atares[i] = responseresv[key]
            i=i+1
    else:
        pass

    caseclsd = frthset.filter(action_type__contains=ActionTypes.CASE_CLOSED)
    if caseclsd.count()!=0:
        clsdres = statechange(caseclsd,caseclsd.count())
        for key in clsdres:
            atares[i]=clsdres[key]
            i=i+1
    else:
        pass

    casereopen=frthset.filter(action_type__contains=ActionTypes.CASE_REOPENED_RA)
    if casereopen.count()!=0:
        reopencase_response=statechange(casereopen, casereopen.count())
        for key in reopencase_response:
            atares[i]=reopencase_response[key]
            i=i+1
    else :
        pass
    casere_investigation=frthset.filter(action_type__contains=ActionTypes.STATUS_PUT,current_state=CaseStatus.RE_INVESTIGATION_RA)
    if casere_investigation.count()!=0:
        reopencase_response=statechange(casere_investigation, casere_investigation.count())
        for key in reopencase_response:
            atares[i]=reopencase_response[key]
            i=i+1
    else :
        pass
    message = frthset.filter(action_type__contains=ActionTypes.CASE_CLOSING_MESSAGE_SENT)
    if message.exists():
        closeMessgae = message.first()
        messageResponse = closingMessage(closeMessgae)
        atares[i] = messageResponse
        i = i + 1
    else :
        pass

    return atares

def UNRESPONSIVE(auditlogs):
    finalset = auditlogs.filter(
        status__in=[
            CaseStatus.UNRESPONSIVE,
        ]
    )
    print("final logs: ",finalset)
    try:
        unresCaseClose = finalset.get(
            action_type__contains="Case Unresponsive"
        )
    except AuditLog.DoesNotExist:
        return None
    response = Unresponsive(unresCaseClose)
    unres = {}
    i=0
    unres[i] = response
    i=i+1
    try:
        unresmsg=finalset.get(action_type__contains="Case Closed Due to Lack of Response, Message sent")
        closemsgResponse=unResponsiveSent(unresmsg)
        unres[i]=closemsgResponse
        i=i+1
    except AuditLog.DoesNotExist:
        pass

    print("unres logs: ",unres)

    return unres



class RoleListAV(APIView):
    def get(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        response=[]
        for i in UserRole:
            if(i!=UserRole.SUPER_ADMIN and i!=UserRole.INACHE_ADMIN and i != UserRole.DEFAULT_ROLE):
                response.append(i)
        if userRole.user_fk.company_fk.Legalcompanyname == "Shahi Exports PVT LTD":
            response.remove(UserRole.FACTORY_ADMIN)
            if userRole.role.role == UserRole.SUPER_ADMIN:
                pass
            elif userRole.role.role == UserRole.REGIONAL_ADMIN:
                response.remove(UserRole.REGIONAL_ADMIN)
        else:
            if userRole.role.role == UserRole.SUPER_ADMIN:
                pass
            elif userRole.role.role == UserRole.REGIONAL_ADMIN:
                response.remove(UserRole.REGIONAL_ADMIN)
            elif userRole.role.role == UserRole.FACTORY_ADMIN:
                response.remove(UserRole.REGIONAL_ADMIN)
                response.remove(UserRole.FACTORY_ADMIN)
        message = {
                    "message": "Roles fetched successfully",

                    "Roles":response
                }

        return Response(message,status.HTTP_200_OK)

class ComplainerViewSet(viewsets.ViewSet):
    # parser_class = (FileUploadParser,)
    permission_classes=[isSAorRA]
    def create(self, request:Request)->Response:
        serializer = CsvSerializer(data=request.data)
        try:
            company=Company.objects.get(id=request.data['Company'])
        except Company.DoesNotExist:
            return Response(
                    {
                        "errorMessage": "Company with ID {} doesn't exist".format(
                            request.data['Company']
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        try:
            factory=Factory.objects.get(id=request.data['Factory'])
        except Factory.DoesNotExist:
            return Response(
                    {
                        "errorMessage": "Factory with ID {} doesn't exist".format(
                            request.data['Factory']
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        if serializer.is_valid():
            csv_file = request.FILES['csv_file']
            csv_data = csv_file.read().decode('utf-8')
            counter,rows=update_complainers(csv_data,request.data['Company'],request.data['Factory'])
            if(counter >=rows):
                return Response(
                    {
                        "errorMessage": "Incorrect Factory data in CSV file"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            message = {
                    "message": "Master Data uploaded for Company {} and Factory {} ".format(
                        request.data['Company'],request.data['Factory']
                    )

                }
            return Response(message,status=status.HTTP_201_CREATED)
        else:
            error_response=serialer_error(serializer.errors)
            return Response(
                            error_response
            ,status=status.HTTP_400_BAD_REQUEST)

def update_complainers(csv_data,Company,Fac):
     # Read the CSV data into a pandas dataframe
    df = pd.read_csv(StringIO(csv_data))

       # Delete complainers not present in the new CSV file
    existing_complainers = Complainer.objects.filter(Factory=Fac,Company=Company)
    existing_emails = set(existing_complainers.values_list('PhoneNo', flat=True))
    #existing_departments = list(set(existing_complainers.values_list('Factory', 'Department', 'SubDepartment')))
    # Iterate over each row in the CSV file
    new_complainers=[]
    new_departments = []
    new_coms={}
    unit=""
    counter=0
    rows=df.shape[0]
    for _, row in df.iterrows():
        (Unit, Department, SubDepartment, Gender, Mobile, Language) = row
        # Check if the complainer already exists in the database
        unit=Unit
        # print(unit)
        new_complainers.append(str(Mobile))
        new_departments.append([Fac,Department,SubDepartment])
        param_factory=Factory.objects.get(id=Fac)
        try:
            csv_factory=Factory.objects.get(Code=Unit)
        except Factory.DoesNotExist:
            counter=counter+1
            continue
        if(csv_factory!=param_factory):
            # print(counter)
            counter=counter+1
            continue
        # print(str(Mobile) in existing_emails)
        if str(Mobile) in existing_emails:
            try:
                complainer = Complainer.objects.get(Factory=Fac,Company=Company,PhoneNo=Mobile)
            except Complainer.MultipleObjectsReturned:
                complainer = Complainer.objects.filter(PhoneNo=Mobile,Factory=Fac,Company=Company).first()
                Complainer.objects.filter(PhoneNo=Mobile).exclude(id=complainer.id).delete()
            # except Complainer.DoesNotExist:
            #     print(Unit, Department, SubDepartment, Gender, Mobile, Language)
            #     break

            complainer.Department=Department
            complainer.SubDepartment=SubDepartment
            complainer.Gender=Gender
            complainer.PhoneNo=Mobile
            complainer.Language=Language
            complainer.Registered=True
            complainer.save()
        else:
            new_coms[Mobile]=Complainer(
                Company_id=Company,
                Factory_id=Fac,
                Department=Department,
                SubDepartment=SubDepartment,
                Gender=Gender,
                PhoneNo=Mobile,
                Language=Language,
                Registered=True
            )

    # print(new_complainers,"dsdsds")
    delete_complainers=[]
    for comp in existing_complainers:
        if str(comp.PhoneNo) not in new_complainers:
            if Case.objects.filter(Complainer=comp,CaseStatus__in=[CaseStatus.ASSIGNED_TO_REPORTER,CaseStatus.ASSIGNED_TO_MANAGER,CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,CaseStatus.RESOLVED,CaseStatus.UNDER_INVESTIGATION,CaseStatus.RE_INVESTIGATION]).exists():
                new_departments.append([comp.Factory.id,comp.Department,comp.SubDepartment])
                continue
            # if comp.Registered == False:
            #     continue
            delete_complainers.append(comp)
            # print(comp)

    unique_lists = [list(t) for t in set(tuple(l) for l in new_departments)]


    for dept in unique_lists:
        try:
            FactoryDepartment.objects.get(factory=Factory.objects.get(id=int(dept[0])),Department=dept[1],SubDepartment=dept[2])
        except:
            FactoryDepartment.objects.create(factory=Factory.objects.get(id=int(dept[0])),Department=dept[1],SubDepartment=dept[2])


    # print(new_coms)
    Complainer.objects.bulk_create(list(new_coms.values()))
    Complainer.objects.filter(pk__in=[complainer.pk for complainer in delete_complainers]).update(is_active=False)
    # print(delete_complainers)
    # print(new_coms)
    # print(new_complainers)
    return counter,rows

# def T0T1T2Breached(case,date):
#     startDate = getattr(case, date)
#     setattr(case, date, current_time())
#     endDate = current_time()
#     days = working_days(startDate, endDate)
#     if case.Breached != True:
#         if days <= 1:
#             case.Breached = None
#         else:
#             case.Breached = True

# def T3Breached(case,date):
#     def Breached(time,deadline):
#         if case.Breached != True:
#             if time <= deadline:
#                 case.Breached = None
#             else:
#                 case.Breached = True
#     startDate = getattr(case, date)
#     setattr(case, date, current_time())
#     endDate = current_time()
#     days = working_days(startDate,endDate)
#     priorities = {"Canteen food":"Medium", "Canteen cleanliness & infrastructure":"Minor", "Factory temperature & conditions":"Medium", "Machine maintenance":"Medium", "PPE":"Minor",
#             "Shop Floor cleanliness":"Minor", "Washroom cleanliness":"Minor", "Leave":"Medium", "Absenteeism":"Medium",
#             "Conflict with People Officer":["Major","Level 1"], "Conflict with co-worker":["Major","Level 1"], "Welfare schemes":"Medium", "Other facilities":"Minor", "Transport":"Minor","Dormitory":"Minor",
#             "PF":"Medium", "ESI":"Medium", "Full and final":"Medium", "Compensation & Benefits":"Medium", "Sexual harassment":"Major", "Case against influential managers":["Major","Level 1"],
#             "Miscellaneous":"Minor", "Dispensary facilities":"Medium"}
#     subcategory=case.SubCategory
#     if priorities[subcategory]=="Minor":
#         if case.Priority == "Minor Grievance (Internal)":
#             sla = 3
#             case.Breached = Breached(days,sla)
#         else:  
#             sla =30
#             case.Breached = Breached(days,sla)
#     elif priorities[subcategory] == "Medium":
#         if case.Priority == "Medium Grievance (Internal)":
#             sla =3
#             case.Breached = Breached(days,sla)
#         else:
#             sla =7
#             case.Breached = Breached(days,sla)
#     elif priorities[subcategory][0] == "Major":
#         if priorities[subcategory][1] == "Level 1":
#             sla =7
#             case.Breached = Breached(days,sla)
#         else:
#             sla =3
#             case.Breached = Breached(days,sla)
#     else: # posh cases will not get affected by changing ct's
#         setattr(case, date, startDate)


# def Breached(time,deadline):
#     if case.Breached != True:
#         if time <= deadline:
#             return None
#         else:
#             return True

class AssignCaseAV(APIView):
    def put(self, request: Request) -> Response:
        fromuser=request.query_params.get("fromRole")
        touser=request.query_params.get("toRole")
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        if not fromuser:
            return Response({'errorMessage':"Please pass the required params"},status=status.HTTP_400_BAD_REQUEST)
        
        if int(fromuser)<0:
            return Response({'errorMessage':"Negitive value is not supported"},status=status.HTTP_400_BAD_REQUEST)
            #dont let neg bvalue come through
        try:
            fromRole=UserRoleFactory.objects.get(id=fromuser,is_active=True)
        except UserRoleFactory.DoesNotExist:
             
             return Response(
                    {
                        "errorMessage": "Role with ID {} doesn't exist".format(
                            fromuser
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

        arg={
                   UserRole.CASE_REPORTER :{
                       'CaseStatus__in':
                           [CaseStatus.ASSIGNED_TO_REPORTER],
                        'CaseReporter':fromRole
                        
                           },
                   UserRole.CASE_MANAGER :{
                       'CaseStatus__in':
                           [CaseStatus.ASSIGNED_TO_MANAGER],
                        'CaseManager':fromRole
                        
                           },
                   UserRole.CASE_TROUBLESHOOTER :{
                       'CaseStatus__in':
                           [CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,CaseStatus.UNDER_INVESTIGATION,CaseStatus.RE_INVESTIGATION,CaseStatus.RESOLVED],
                        'CaseTroubleShooter':fromRole
                        
                           },
                   UserRole.REGIONAL_ADMIN :{
                       'CaseStatus__in':[CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN,CaseStatus.RA_INVESTIGATION,CaseStatus.RE_INVESTIGATION_RA,CaseStatus.RESOLVED],
                        'RegionalAdmin':fromRole
                        
                           },
                }
        query_args=arg.get(fromRole.role.role)
        print(query_args)
        #if query_args is empty then trrow a error in reponse
        if query_args is None and (request.query_params.get("operation") == "merge-case" or request.query_params.get("operation") == "split-case") :
            return Response(

                    {
                        "errorMessage": "Role is {} not authorized to access this API".format(
                            fromRole.role.role
                        )
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        cases=Case.objects.filter(**query_args)
        if cases.count()==0 and (request.query_params.get("operation") == "merge-case" or request.query_params.get("operation") == "split-case"):
            fromRole.is_active=False
            fromRole.save()
            if UserRoleFactory.objects.filter(user_fk=fromRole.user_fk,is_active=True).exists() == False:
                fromRole.user_fk.is_active=False
                fromRole.user_fk.save()
            return Response(
                {
                    "message": "User {} doesn't does not have active cases but has been deleted".format(
                            fromRole.user_fk.user_name
                    ),
                    "statusCode":"no_cases"
                },
                status=status.HTTP_200_OK,
            )
        if request.query_params.get("operation")=="merge-case":
            message,response_status=merge_case(fromuser,fromRole,touser,cases,userRole)
            return Response(message,status=response_status)
        elif request.query_params.get("operation")=="split-case":
            message,response_status = split_cases(fromRole,request, cases,userRole)
            return Response(message,status=response_status)
        elif request.query_params.get("operation")=="assign-case":
            message,response_status = assign_cases(touser,fromRole,cases,userRole)
            return Response(message,status=response_status)

        else:
            return Response({'errorMessage':"Please pass a valid Operation"},status=status.HTTP_400_BAD_REQUEST)

class CaseFilter(APIView):

    def get(self, request: Request) -> Response:
        queryset = Case.objects.all()

        # Get the company ID and factory ID from query parameters
        company_id = self.request.query_params.get('company')
        factory_id = self.request.query_params.get('factory')

        # Apply filters to the queryset
        if company_id:
            queryset = queryset.filter(Company=company_id)
        if factory_id:
            queryset = queryset.filter(Factory=factory_id)
        if queryset.count()==0:
            return Response(
                {
                        "errorMessage": "Cases doesn't exist"
                    },
                    status=status.HTTP_404_NOT_FOUND,
            )
        serializer=CaseSerializers(queryset,many=True)
        message = {
                    "message": "Cases fetched successfully",
                    "message_body" :serializer.data
                }
        return Response(message,status=status.HTTP_200_OK)


        


# class sanitizedata(APIView):
#     def get(self,request):
#         users = BaseUserModel.objects.all()
#         for user in users:
#             if user.role == UserRole.CASE_REPORTER:
#                 try:
#                     cr=CaseReporter.objects.get(id=user.id)
#                 except:
#                     pass
#                 user.company_fk=cr.Company
#                 user.factory_fk=cr.Factory
#                 group = Group.objects.get(name='CR')
#                 user.groups.add(group)
#             if user.role == UserRole.CASE_MANAGER:
#                 try:
#                     cm=CaseManager.objects.get(id=user.id)
#                 except:
#                     pass
#                 user.company_fk=cm.Company
#                 user.factory_fk=cm.Factory
#                 group = Group.objects.get(name='CM')
#                 user.groups.add(group)
#             if user.role == UserRole.CASE_TROUBLESHOOTER:
#                 try:
#                     ct=CaseTroubleShooter.objects.get(id=user.id)
#                 except:
#                     pass
#                 user.company_fk=ct.Company
#                 user.factory_fk=ct.Factory
#                 group = Group.objects.get(name='CT')
#                 user.groups.add(group)
#             if user.role == UserRole.FACTORY_ADMIN:
#                 group = Group.objects.get(name='FACTORY_ADMIN')
#                 user.groups.add(group)
#             if user.role == UserRole.SUPER_ADMIN:
#                 group = Group.objects.get(name='SUPER_ADMIN')
#                 user.groups.add(group)
#             user.save()
#         # Repeat the above steps for each role and corresponding group
        
#         return HttpResponse('Group assigned to user successfully.')
    


class CTMessageDraft(APIView):
    def get(self, request: Request) -> Response:
        company = request.user.company_fk.id
        # factory = request.user.factory_fk.id
        # print("company is:",company)
        # print("factory is:",factory)
        # if request.user.role == UserRole.CASE_REPORTER:
        #     factory = CaseReporter.objects.get(id=request.user.id).Factory.id
        #     company = CaseReporter.objects.get(id=request.user.id).Company.id
        #     print("factory is:",factory)
        # elif request.user.role == UserRole.CASE_MANAGER:
        #     factory = CaseManager.objects.get(id=request.user.id).Factory.id
        #     company = CaseManager.objects.get(id=request.user.id).Company.id
        #     print("factory is:",factory)
        # elif request.user.role == UserRole.CASE_TROUBLESHOOTER:
        #     factory = CaseTroubleShooter.objects.get(id=request.user.id).Factory.id
        #     company = CaseTroubleShooter.objects.get(id=request.user.id).Company.id
        #     print("factory is:",factory)
        #draft = BroadcastMessage.objects.get(id=request.query_params.get("draftID"))
        draft = BroadcastMessage.objects.filter(status=Status.CTDRAFT,sendCount=request.query_params.get("caseID")).latest("lastModified")
        serializer = BroadcastMessageSerializer(draft)
        variables = json.loads(SMSTemplates.objects.get(templateID=serializer.data["templateIDs"][0],Company=company).variables)
        inputs = serializer.data["inputVariables"]
        list = []
        for key,value in variables.items():
            list.append({"var":{key:value},"InputValue":inputs[value],"language":serializer.data['Languages']})
        message = {
                        "message": "Draft with draftID {} has been fetched successfully".format(
                            serializer.data["id"]
                        ),
                        "message_body": {"Status":serializer.data["status"],"draftID":serializer.data["id"],"templateIDs":serializer.data["templateIDs"],"language":serializer.data["Languages"],"Template":serializer.data["templateTitle"],"variables":list,"Message":serializer.data['messageBody'][0]["body"]},
                    }
        return Response(message, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        user_id = userRole.id
        cache_key = f'user_data_{user_id}_first'
        data = cache.get(cache_key)
        if data == None:
            return Response(
                {
                    "errorMessage": "No Cache Data found"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        message = data['templates']
        body = []
        templateIDs = []
        for templates in message:
            body.append(templates)
            templateIDs.append(templates["templateID"])
        draft = BroadcastMessage.objects.create(
            createdBy =  request.user.user_name + " (" + userRole.role.role + ")",
            Languages = data['language'],
            templateTitle = message[0]["Title"],
            messageBody = body,
            Factory = Factory.objects.get(id=data['factory']),
            status = Status.CTDRAFT,
            templateIDs = list(set(templateIDs)),
            inputVariables = data['inputs'],
            sendCount = data['caseID']
        )
        draft.save()
        cache.delete(cache_key)  # Delete data from cache
        serializer = BroadcastMessageSerializer(draft)
        message = {
            "message": "A Draft with draftID {} is created successfully".format(
                serializer.data["id"]
            ),
            "message_body": serializer.data,
        }
        return Response(message, status=status.HTTP_201_CREATED)

    def patch(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        user_id = userRole.id
        cache_key = f'user_data_{user_id}_first'
        data = cache.get(cache_key)
        if data == None:
            return Response(
                {
                    "errorMessage": "No Cache Data found"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        message = data['templates']
        templateIDs = []
        for templates in message:
            templateIDs.append(templates["templateID"])
        try:
            # draft = BroadcastMessage.objects.get(
            #     id=request.query_params.get("draftID")
            # )
            draft = BroadcastMessage.objects.filter(status=Status.CTDRAFT,sendCount=request.query_params.get("caseID")).latest("lastModified")
            serializer = BroadcastMessageSerializer(draft)
            draftSerializer = serializer.data
            draftSerializer["lastModified"] = current_time()
            draftSerializer["Languages"] = data['language']
            draftSerializer["messageBody"] = data['templates']
            draftSerializer["templateIDs"] = list(set(templateIDs))
            draftSerializer["inputVariables"] = data['inputs']
            draftSerializer["Genders"] = ["None"]
            draftSerializer["departments"] = ["None"]
            serializer = BroadcastMessageSerializer(
                draft, data=draftSerializer, partial=True
            )
            cache.delete(cache_key)  # Delete data from cache
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = {
                    "message": "Draft with DraftID {} has been updated successfully".format(
                        serializer.data["id"]
                    ),
                    "message_body": serializer.data,
                }
                return Response(message, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except BroadcastMessage.DoesNotExist:
            return Response(
                {
                    "errorMessage": "Draft with ID {} doesn't exist".format(
                        request.query_params.get("draftID")
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request: Request) -> Response:
        try:
            draft = BroadcastMessage.objects.get(
                id=request.query_params.get("draftID")
            )
            draft.delete()
            message = {
                "message": "Draft with ID {} has been Deleted successfully".format(
                    request.query_params.get("draftID")
                )
            }
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        except BroadcastMessage.DoesNotExist:
            return Response(
                {
                    "errorMessage": "Draft with ID {} doesn't exist".format(
                        request.query_params.get("draftID")
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

@api_view(["GET"])
def sanitiseCases(request:Request)->Response:
    cases=Case.objects.filter(T1vrfDate=None)
    for case in cases:
        case.T1vrfDate = case.Date
        case.save()
    return Response("Cases cleaned")

#TODO : Need to remove this after 20th June 2023
@api_view(["GET"])
def sanitiseUserPermissions(request:Request)->Response:
    users=BaseUserModel.objects.filter(is_active=True)
    for user in users:
        # del user._perm_cache
        # del user._user_perm_cache
        for permission in user.user_permissions.all():
            pass
        if user.has_perm("accounts.view_holiday_calender"):
            permission = Permission.objects.get(codename="view_holiday_calender")
            user.user_permissions.remove(permission)
            permission = Permission.objects.get(codename="view_holidaycalendar")
            user.user_permissions.add(permission)
        if user.has_perm("accounts.change_holiday_calender"):
            permission = Permission.objects.get(codename="change_holiday_calender")
            user.user_permissions.remove(permission)
            permission = Permission.objects.get(codename="change_holidaycalendar")
            user.user_permissions.add(permission)
        if user.has_perm("accounts.delete_holiday_calender"):
            try:
                permission = Permission.objects.get(codename="delete_holiday_calender")
            except Permission.DoesNotExist:
                pass
            user.user_permissions.remove(permission)
            permission = Permission.objects.get(codename="delete_holidaycalendar")
            user.user_permissions.add(permission)
        if user.has_perm("accounts.add_holiday_calender"):
            permission = Permission.objects.get(codename="add_holiday_calender")
            user.user_permissions.remove(permission)
            permission = Permission.objects.get(codename="add_holidaycalendar")
            user.user_permissions.add(permission)
        if user.role==UserRole.CASE_MANAGER or user.role==UserRole.CASE_REPORTER or user.role==UserRole.CASE_TROUBLESHOOTER:
            permission = Permission.objects.get(codename="view_holidaycalendar")
            user.user_permissions.add(permission)
    return(Response("Permissions cleaned"))


@api_view(['GET'])

def sanitizeRoles(request:Request)->Response:
    users=BaseUserModel.objects.all()
    groups=Group.objects.all()
    for group in groups:
        role,created=Role.objects.get_or_create(role=group.name)
        role.group_permissions.add(group)
        role.full_clean()
        role.save()
    for user in users:
        print(user,"BUM")
        try:
            role=UserRoleFactory.objects.create(user_fk=user, role=Role.objects.get(role=user.role),factory_fk=user.factory_fk,is_active=user.is_active)
            permissions=user.user_permissions.all()
            for permission in permissions:
                role.user_permissions.add(Permission.objects.get(codename=permission.codename))
            role.save()
        except Role.DoesNotExist:
            continue
    return Response("Done")


@api_view(['GET'])
def sanitizerinactiveoles(request): 
    users=BaseUserModel.objects.all()
    for user in users:
        if user.is_active==False:
            print(user,"user")
            roles=UserRoleFactory.objects.filter(user_fk=user)
            for role in roles:
                print(role,"role`",role.is_active)
                role.is_active=False
                role.save()
        
    return Response("Done")
@api_view(['GET'])
def sanitizeCases(request:Request)->Response:
    cases=Case.objects.all()
    auditlogs=AuditLog.objects.all()
    for al in auditlogs:
        created_by=al.created_by
        # cb=BaseUserModel.objects.get(id= created_by.id)
        print(created_by)
        rolecb=UserRoleFactory.objects.get(user_fk__id=created_by.id)
        al.uploaded_by=rolecb
        al.save()
    files3=UploadedFile_S3.objects.all()
    for file in files3:
        try:
            created_by=file.uploaded_by
            # cb=BaseUserModel.objects.get(id= created_by.id)
            print(created_by)
            rolecb=UserRoleFactory.objects.get(user_fk__id=created_by.id)
            file.created_by=rolecb
            file.save()
        except :
            pass
        
    # for case in cases:
        
    #     # try:
    #     print(case)
    #     cr=(case.CaseReporter_id)
    #     print((case.CaseReporter_id),"casecr")
    #     if cr is not None :
    #         try:
    #             cr=BaseUserModel.objects.get(id=case.CaseReporter_id)
    #             print(cr,"bum")
    #             usercr=UserRoleFactory.objects.get(user_fk__id=cr.id,factory_fk=cr.factory_fk,role__role=cr.role)
    #             case.CaseReporter=usercr
    #             case.save()
    #         except BaseUserModel.DoesNotExist:
    #             print("pass bum")
    #             pass
    #         except UserRoleFactory.DoesNotExist:
    #             print("pass urf")
    #             pass
    #     else:
    #         pass
    #     cm=case.CaseManager_id
    #     print(cm,"casecm")
    #     if cm is not None :
    #         try:
    #             cm=BaseUserModel.objects.get(id=case.CaseManager_id)
    #             print(cm,"bum")
    #             usercm=UserRoleFactory.objects.get(user_fk__id=cm.id,factory_fk=cm.factory_fk,role__role=cm.role)
    #             case.CaseManager=usercm
    #             case.save()

    #         except BaseUserModel.DoesNotExist:
    #             print("pass")
    #             pass
    #         except UserRoleFactory.DoesNotExist:
    #             print("pass urf")
    #             pass
    #     else:
    #         pass
    #     ct=case.CaseTroubleShooter_id
    #     print(ct,"caseCT")
    #     if ct is not None :
    #         try:
    #             ct=BaseUserModel.objects.get(id=case.CaseTroubleShooter_id)
    #             print(ct,"bum")
    #             userct=UserRoleFactory.objects.get(user_fk__id=ct.id,factory_fk=ct.factory_fk,role__role=ct.role)
    #             case.CaseTroubleShooter=userct
    #             case.save()
    #         except BaseUserModel.DoesNotExist:
    #             print("pass")
    #             pass
    #         except UserRoleFactory.DoesNotExist:
    #             print("pass urf")
    #             pass
    #     pass
    #     # except :
    #     #     pass
    #     case.save()
    return Response("done")
    
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request:Request, *args, **kwargs:any)->Response:
        try:
            response = super().post(request, *args, **kwargs)

            # Customize the response data
            if response.status_code == 200:
                # Extract the token and user from the response data
                token = response.data.get('access')
                user=BaseUserModel.objects.get(email=request.data['email'],is_active=True)
                userserialzer=BaseUserModelSerializer(user)
                data={'roles':{},"userData":userserialzer.data,"tokens":response.data,"atLogin":{}}

                roles=UserRoleFactory.objects.filter(user_fk=user,is_active=True)
                perms = []
                for role in roles:
                    roleperms={}
                    perms=[]
                    permissions = role.user_permissions.all()
                    key=str(role.role)+"_"+str(role.factory_fk)
                    data['roles'][key]={}
                    for perm in permissions:
                        perms.append(perm.codename)
                    roleperms['user_permissions'] = (perms)
                    roleperms['role'] = str(role.role)
                    roleperms['id']=role.id
                    if role.role.role==UserRole.REGIONAL_ADMIN:
                        roleperms["region_fk"] = role.region_fk.id
                        roleperms["region"] = role.region_fk.Name
                    elif role.role.role==UserRole.SUPER_ADMIN:
                        pass
                    else:
                        roleperms["factory_fk"] = role.factory_fk.id
                        roleperms["Code"] = str(role.factory_fk.Code)
                        roleperms["Location"] = str(role.factory_fk.Location)
                        roleperms["region"] = role.factory_fk.region.Name
                    roleobj=Role.objects.get(pk=role.role.id)
                    grp_permissions = get_group_permissions(roleobj.group_permissions.all())
                    grp_perms = []

                    if grp_permissions is not None:
                        for permission in grp_permissions:
                            grp_perms.append(permission.codename)
                    else:
                        pass
                    # This code calls the get_group_permissions function with the name of the group you want to retrieve permissions for. If the group is found, it loops through the retrieved Permission objects and prints their codename attribute. If the group is not found, it prints a message indicating that the group was not found.
                    roleperms['group_permissions'] = grp_perms
                    data['roles'][key]=(roleperms)
                if(request.data['password']=="vouge2023/"):
                    data['atLogin']["render_reset_password"] =  "true"
                else:
                    data['atLogin']["render_reset_password"] =  "false"
                if user.language == None:
                    data['atLogin']["language_preference_needed"] = "true"
                else:
                    data['atLogin']["language_preference_needed"] = "false"
            return Response(data)
    
        except Exception as e:

            if 'No active account found' in str(e):
                
                email = request.data['email']
                if BaseUserModel.objects.filter(email=email, is_active=False).exists():
                    return Response({"error": "Account has no active roles, please create one to login"}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({"error": "Login Failed, Please check the credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(["POST"])       
def encodeID(request: HttpRequest)-> Response:
    token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[1]
    refresh = request.data.get("refresh")
    id=request.query_params.get("role_id")
    secret_key =settings.base.SECRET_KEY
    if id is None:
        return Response({"errorMessage": "Role ID is required"},status=status.HTTP_400_BAD_REQUEST)
    try:
        userRole=UserRoleFactory.objects.get(id=id)
    except UserRoleFactory.DoesNotExist:
        return Response({"errorMessage": "Role ID does not exist"},status=status.HTTP_404_NOT_FOUND)
    # if userRole.user_fk.id != request.user.id:
    #     return Response({"errorMessage": "Role does not belong to the user"},status=status.HTTP_403_FORBIDDEN)
    new_data = {
    "role_id": id
    }

    # Decode the existing token
    decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
    decoded_refresh_token = jwt.decode(refresh, secret_key, algorithms=["HS256"])

    # Update the token's payload with new information
    decoded_token.update(new_data)
    decoded_refresh_token.update(new_data)

    # Encode the updated token with the sec_ret key
    updated_token = jwt.encode(decoded_token, secret_key, algorithm="HS256")
    updated_refresh_token = jwt.encode(decoded_refresh_token, secret_key, algorithm="HS256")
    data={"access": updated_token , "refresh": updated_refresh_token}
    userRole.last_login_role = timezone.now()
    userRole.save()
    return Response(data)



@api_view(["GET"])
def sanitiseIncentives(request):
    cases=Case.objects.all()
    for case in cases:
        try:
            Incentives.objects.get(Case=case)
        except:
            Incentives.objects.create(Case=case)
    return Response("Incentives cleaned")


@api_view(["GET"])
def sanitizeRA(request):
    rausers=UserRoleFactory.objects.filter(role__role=UserRole.REGIONAL_ADMIN)
    for user in rausers:
        if user.factory_fk is not None:
            factory=Factory.objects.get(id=user.factory_fk.id)
            user.region_fk=factory.region
            user.factory_fk=None
            user.save()  
    return Response("RA cleaned")         


@api_view(["GET"])
def patchRA(request):
    rausers=UserRoleFactory.objects.filter(role__role=UserRole.REGIONAL_ADMIN)
    for user in rausers:
        if user.factory_fk is None:
            factory=Factory.objects.filter(region=user.region_fk).first()
            user.factory_fk=factory
            user.save()  
    return Response("RAs factory patched")           
            


#TODO: Need to remove this
@api_view(["GET"])
def sanitizeprofilepics(request):
    users=BaseUserModel.objects.filter(is_active=True)
    for user in users:
        file=UploadedFile_S3.objects.get(s3_file_path__contains="default.png")
        try:
            profile_pic=User_Profilepic.objects.get(user_id=user.id)
        except User_Profilepic.DoesNotExist:
            profile_pic=User_Profilepic.objects.create(user_id=user.id)
        profile_pic.profile_picture=file
        profile_pic.save()
    return Response("Profile pics cleaned")


@api_view(["GET"])
def sanitizeSA(request):
    sausers=UserRoleFactory.objects.filter(role__role=UserRole.SUPER_ADMIN)
    for user in sausers:
        if user.factory_fk is not None:
            user.factory_fk=None
            user.save()  
    return Response("SA cleaned")  


@api_view(["GET"])
def sanitizeBaseUsers(request):
    users=BaseUserModel.objects.all()
    for user in users:
        if user.factory_fk is not None:
            user.factory_fk=None
            user.save()  
    return Response("Base users cleaned")  


@api_view(["GET"])
def sanitizeuserpermissions(request): 
        
    users=UserRoleFactory.objects.all()
    for user in users:
        
        
        if user.role.role==UserRole.REGIONAL_ADMIN or user.role.role==UserRole.SUPER_ADMIN or user.role.role==UserRole.CASE_MANAGER or user.role.role==UserRole.FACTORY_ADMIN:
            perms=user.user_permissions.all()
            for perm in perms:
                print(perm)
                user.user_permissions.remove(perm)
        #remove underscore from perms when pushing to stage
        if user.role.role==UserRole.CASE_REPORTER or user.role.role==UserRole.CASE_TROUBLESHOOTER:
            if user.has_perm("add_broadcast_message") :
                print("Adding broadcast message permission")
                remaddbmperm=Permission.objects.get(codename="add_broadcast_message")
                user.user_permissions.remove(remaddbmperm) 
            if user.has_perm("delete_holidaycalendar") :
                print("deleting holiday calendar permission")
                remaddhcperm=Permission.objects.get(codename="delete_holidaycalendar")
                user.user_permissions.remove(remaddhcperm) 
            if user.has_perm("change_broadcast_message") :
                print("changing broadcast message permission")
                remchbmperm=Permission.objects.get(codename="change_broadcast_message")
                user.user_permissions.remove(remchbmperm) 
            if user.has_perm("view_broadcast_message") :
                print("viewing broadcast message permission")     
                remviewbmperm=Permission.objects.get(codename="view_broadcast_message")
                user.user_permissions.remove(remviewbmperm)         
            if user.has_perm("add_broadcastmessage") :
                print("Adding broadcast message permission")
                remaddbmperm=Permission.objects.get(codename="add_broadcastmessage")
                user.user_permissions.remove(remaddbmperm)   
            if user.has_perm("change_broadcastmessage") :
                print("changing broadcast message permission")
                remchbmperm=Permission.objects.get(codename="change_broadcastmessage")
                user.user_permissions.remove(remchbmperm) 
            if user.has_perm("view_broadcastmessage") :
                print("viewing broadcast message permission")     
                remviewbmperm=Permission.objects.get(codename="view_broadcastmessage")
                user.user_permissions.remove(remviewbmperm)         
            if user.has_perm("add_holiday_calendar") :
                print("Adding holiday permission")
                remaddhcperm=Permission.objects.get(codename="add_holiday_calendar")
                user.user_permissions.remove(remaddhcperm)         
            if user.has_perm("change_holiday_calendar"):
                print("changing holiday permission")
                remchhcperm=Permission.objects.get(codename="change_holiday_calendar")
                user.user_permissions.remove(remchhcperm)
            if user.has_perm("view_holiday_calendar"):
                print("viewling holiday permission")
                remviewhcperm=Permission.objects.get(codename="view_holiday_calendar")
                user.user_permissions.remove(remviewhcperm)
            if user.has_perm("add_holidaycalendar") :
                print("Adding holiday permission")
                remaddhcperm=Permission.objects.get(codename="add_holidaycalendar")
                user.user_permissions.remove(remaddhcperm)         
            if user.has_perm("change_holidaycalendar"):
                print("changing holiday permission")
                remchhcperm=Permission.objects.get(codename="change_holidaycalendar")
                user.user_permissions.remove(remchhcperm)
            if user.has_perm("view_holidaycalendar"):
                print("viewling holiday permission")
                remviewhcperm=Permission.objects.get(codename="view_holidaycalendar")
                user.user_permissions.remove(remviewhcperm)
            if user.has_perm("add_awareness_program") :
                print("assing awareness permission")
                remaddapperm=Permission.objects.get(codename="add_awareness_program")
                user.user_permissions.remove(remaddapperm)
                addappermission = Permission.objects.get(codename='add_awarenessprogram')
                user.user_permissions.add(addappermission)
            if user.has_perm("change_awareness_program"):
                print("changing awareness permission")
                remchapperm=Permission.objects.get(codename="change_awareness_program")
                user.user_permissions.remove(remchapperm)
                changeappermission = Permission.objects.get(codename='change_awarenessprogram')
                user.user_permissions.add(changeappermission)
            if user.has_perm("view_awareness_program"):
                print("viewing awareness permission")
                remviewapperm=Permission.objects.get(codename="view_awareness_program")
                user.user_permissions.remove(remviewapperm)
                viewappermission = Permission.objects.get(codename='view_awarenessprogram')
                user.user_permissions.add(viewappermission)
            
            
            
            #------------------------------------
        # print(user.user_permissions.all())
        # if user.has_perm("add_broadcast_message"):
        #     print("Adding broadcast message permission")
        #     remaddbmperm=Permission.objects.get(codename="add_broadcast_message")
        #     user.user_permissions.remove(remaddbmperm)
        #     addbmpermission = Permission.objects.get(codename='add_broadcastmessage')
        #     user.user_permissions.add(addbmpermission)
        # if user.has_perm("change_broadcast_message"):
        #     print("changing broadcast message permission")
        #     remchbmperm=Permission.objects.get(codename="change_broadcast_message")
        #     user.user_permissions.remove(remchbmperm)
        #     changebmpermission = Permission.objects.get(codename='add_broadcastmessage')
        #     user.user_permissions.add(changebmpermission)
        # if user.has_perm("view_broadcast_message"):
        #     print("viewing broadcast message permission")
        #     remviewbmperm=Permission.objects.get(codename="view_broadcast_message")
        #     user.user_permissions.remove(remviewbmperm)
        #     viewbmpermission = Permission.objects.get(codename='add_broadcastmessage')
        #     user.user_permissions.add(viewbmpermission)
        # if user.has_perm("add_holiday_calender") or user.has_perm("add_holiday_calendar"):
        #     print("Adding holiday permission")
        #     remaddhcperm=Permission.objects.get(codename="add_holiday_calendar")
        #     user.user_permissions.remove(remaddhcperm)
        #     addhcpermission = Permission.objects.get(codename='add_holidaycalendar')
        #     user.user_permissions.add(addhcpermission)
        # if user.has_perm("change_holiday_calender")or user.has_perm("change_holiday_calendar"):
        #     print("changing holiday permission")
        #     remchhcperm=Permission.objects.get(codename="change_holiday_calendar")
        #     user.user_permissions.remove(remchhcperm)
        #     chnagehcpermission = Permission.objects.get(codename='change_holidaycalendar')
        #     user.user_permissions.add(chnagehcpermission)
        # if user.has_perm("view_holiday_calender")or user.has_perm("view_holiday_calendar"):
        #     print("viewling holiday permission")
        #     remviewhcperm=Permission.objects.get(codename="view_holiday_calendar")
        #     user.user_permissions.remove(remviewhcperm)
        #     viewhcpermission = Permission.objects.get(codename='view_holidaycalendar')
        #     user.user_permissions.add(viewhcpermission)
        # if user.has_perm("add_awareness_program"):
        #     print("assing awareness permission")
        #     remaddapperm=Permission.objects.get(codename="add_awareness_program")
        #     user.user_permissions.remove(remaddapperm)
        #     addappermission = Permission.objects.get(codename='add_awarenessprogram')
        #     user.user_permissions.add(addappermission)
        # if user.has_perm("change_awareness_program"):
        #     print("changing awareness permission")
        #     remchapperm=Permission.objects.get(codename="change_awareness_program")
        #     user.user_permissions.remove(remchapperm)
        #     changeappermission = Permission.objects.get(codename='change_awarenessprogram')
        #     user.user_permissions.add(changeappermission)
        # if user.has_perm("view_awareness_program"):
        #     print("viewing awareness permission")
        #     remviewapperm=Permission.objects.get(codename="view_awareness_program")
        #     user.user_permissions.remove(remviewapperm)
        #     viewappermission = Permission.objects.get(codename='view_awarenessprogram')
        #     user.user_permissions.add(viewappermission)
        
        
        
        
                    # print("Change broadcast message")
            
        # else:
        #     print("dsdsd")
    return Response("Permissions Sanitized")
    
           
#TODO: Need to remove this
@api_view(["GET"])
def sanitizecasevalidations(request):
    cases = Case.objects.filter(CaseStatus=CaseStatus.CLOSED)
    for case in cases:
        if case.CaseValidation == False and case.CaseCategory == None:
            case.CaseCategory = "Invalid"
        elif case.CaseCategory == "Invalid" and case.CaseValidation == True:
            case.CaseValidation = False
        case.save()
    return Response("case categories and validations are in sync")

#TODO: Need to remove this
@api_view(["GET"])
def gender_sanitize_api(request):
    users = BaseUserModel.objects.filter(gender=0)
    for user in users:
        user.gender = Gender.MALE
        user.save()
    
    users = BaseUserModel.objects.filter(gender=1)
    for user in users:
        user.gender = Gender.FEMALE
        user.save()
    return Response("success, genders sanitized")

        
from django.core.signing import Signer


def unsubscribe_view(request, token):
    try:
        user_id = Signer().unsign(token)
        user = get_object_or_404(BaseUserModel, id=user_id)
        user.unsubscribe = True
        user.save()
        # return render(request, 'unsubscribe_success.html')
        return Response("success")
    except (BadSignature, SignatureExpired, BaseUserModel.DoesNotExist):
        # return render(request, 'unsubscribe_error.html')
        return Response("success")

