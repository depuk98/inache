import json
from django.db import models
from django.db.models.fields import CharField, DateField, IntegerField
import uuid
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,Group,Permission
from django.contrib.postgres.fields import ArrayField
from django.contrib import admin
from django.core.cache import cache

import pytz
from django.contrib.auth.signals import user_logged_in
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator

from django.db.models.signals import post_save, pre_save
from django.utils.translation import gettext as _
from django.dispatch import receiver
from django.conf import settings
from datetime import datetime
from accounts.constants import ActionTypes, ReportingMedium, Gender, CaseStatus, CaseNature, Language, Region, UserRole, Status, \
    CaseActiveStatus, scheduleType
from django.forms import ClearableFileInput, FileField, MultipleChoiceField, MultiValueField
from django.forms.widgets import MultiWidget
# from django import forms


# from django.utils import timezone
# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


def user_directory_path(instance, filename):
    return 'uploads/users/user_{0}/{1}'.format(instance.id, filename)

# class UserModel(AbstractBaseUser, PermissionsMixin):
#     name=models.CharField( max_length=50)
#     # objects = CustomUserManager()
#     USERNAME_FIELD = 'name'


class Company(models.Model):
    Legalcompanyname = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    POC = models.CharField(max_length=50)
    Email = models.EmailField(max_length=254)
    PhoneNo = models.CharField(max_length=15)
    Code = models.CharField(max_length=10, default="")
    SenderID = models.CharField(default="INACHE", max_length=10)
    # FactoryId = models.IntegerField()

    def __str__(self):
        return self.Legalcompanyname

class FactoryRegion(models.Model):
    Name = models.CharField(max_length=100)
    last_modified = models.DateTimeField(default=timezone.localtime, blank=True)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name + " " + str(self.Company)

class Factory(models.Model):
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)
    Code = models.CharField(max_length=10, default="", unique=True)
    Location = models.CharField(max_length=30)
    Region = models.CharField(
        choices=Region.choices, default=Region.SOUTH, max_length=15,
    )
    region = models.ForeignKey(FactoryRegion, null=True, blank=True, on_delete=models.SET_NULL)
    Number = models.CharField(max_length=12, default="")
    requiredAwarenessProgram = models.IntegerField(default=4)
    is_active = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Location + " " + str(self.Code)


class BaseUserModel(AbstractBaseUser,PermissionsMixin):

    name = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=True, unique=True)
    mobile_number = CharField(max_length=15, blank=True)
    password = models.CharField(max_length=100)

    # address = OneToOneField(Address, on_delete=models.CASCADE, null=True)
    user_name = CharField(max_length=255, null=True, unique=True)
    # profile_image = models.ImageField(null=True, storage=PrivateMediaStorage())
    role = models.CharField(
        choices=UserRole.choices, default=UserRole.DEFAULT_ROLE, max_length=64
    )
    date_of_birth = DateField(null=True)
    gender = CharField( choices=Gender.choices,
        default=Gender.NOT_SPECIFIED,
        max_length=20,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    company_fk=models.ForeignKey(Company, null=True, blank=True,on_delete=models.SET_NULL)
    factory_fk=models.ForeignKey(Factory, null=True, blank=True,on_delete=models.SET_NULL)
    
    # profile_picture = models.FileField(
    #     upload_to=user_directory_path, null=True, blank=True, default='uploads/users/default.png')
    # profile_picture=models.OneToOneField(Documents,)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    created_by = models.CharField(
        default="", blank=True, null=True, max_length=200)
    objects = CustomUserManager()
    
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    language = models.JSONField(default=None, null=True)

    # Soft delte or hard delete

    class Meta:
        permissions = (

                        ("view_awareness_program", "view awareness program"),
                        ("add_awareness_program", "add awareness program"),
                        ("change_awareness_program", "change awareness program"),
                        ("view_broadcast_message", "view broadcast message"),
                        ("add_broadcast_message", "add broadcast message"),
                        ("change_broadcast_message", "change broadcast message"),
                        ("crud_factory_admin","crud factory admin"),
                        ("crud_cr","crud case reporter"),
                        ("crud_cm","crud case manager"),
                        ("crud_ct","crud case troubleshooter"),
                        )

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(BaseUserModel, self).save(*args, **kwargs)

class Role(models.Model):
    role = models.CharField(
        choices=UserRole.choices, default=UserRole.DEFAULT_ROLE,max_length=64,unique=True
    )
    group_permissions=models.ManyToManyField(Group)
    
    def __str__(self):
        return self.role
    
class UserRoleFactory(models.Model):
    user_fk = models.ForeignKey(BaseUserModel, on_delete=models.CASCADE)
    role = models.ForeignKey(Role,on_delete=models.SET_NULL,null=True)
    user_permissions = models.ManyToManyField(Permission)
    factory_fk = models.ForeignKey(Factory, on_delete=models.CASCADE, null=True)
    region_fk = models.ForeignKey(FactoryRegion, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)  # Automatically set the field at object creation
    is_active = models.BooleanField(default=True)
    last_login_role= models.DateTimeField(blank=True, null=True)
    IsUnsubscribed = models.BooleanField(default=False)
    def __str__(self):
        return str(self.role )+ str(self.user_fk) + str(self.factory_fk)
    def has_perm(self, perm):
        permission_instances = self.user_permissions.all()
        permission_codenames_list = [permission.codename for permission in permission_instances]
        if perm in permission_codenames_list:
            return True
    class Meta:
        unique_together = (('user_fk', 'role','factory_fk'),)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(UserRoleFactory, self).save(*args, **kwargs)
    

class UploadedFile_S3(models.Model):
    s3_file_path=models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)
    upload_finished_at = models.DateTimeField(blank=True, null=True)
    uploaded_by = models.ForeignKey(UserRoleFactory, on_delete=models.SET_NULL, null= True, blank= True)
    # created_by = models.ForeignKey(
    #     UserRoleFactory, on_delete=models.CASCADE, related_name="cretby",null=True,blank=True)
    


    @property
    def is_valid(self):

        return bool(self.upload_finished_at)

    @property
    def url(self):
        if settings.FILE_UPLOAD_STORAGE == "s3":
            return self.file.url

        return f"{settings.APP_DOMAIN}{self.file.url}"
class User_Profilepic(models.Model):
    user=models.OneToOneField(BaseUserModel,on_delete=models.CASCADE,null=True)
    profile_picture=models.ForeignKey(UploadedFile_S3,on_delete=models.CASCADE,null=True)
class FactoryDepartment(models.Model):
    Department = models.CharField(max_length=50)
    SubDepartment = models.CharField(max_length=50)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)


def program_directory_path(instance, filename):
    return "uploads/programs/program_{0}/{1}".format(instance.id, filename)


class AwarenessProgram(models.Model):
    programNumber = models.CharField(max_length=50, blank=True, null=True)
    programName = models.CharField(max_length=30)
    programDuration = models.IntegerField()
    participants = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999)])
    Date = models.DateTimeField(null=True, blank=True)
    uploadedAt = models.DateTimeField(default=timezone.localtime, blank=True)
    Agenda = models.CharField(max_length=100)
    Description = models.CharField(max_length=1000, blank=True)
    programStatus = models.JSONField(default=None, null=True)
    Reason = models.CharField(max_length=1000, blank=True)
    Breached = models.BooleanField(default=False)
    # user_id = models.ForeignKey(BaseUserModel, null=True, on_delete=models.SET_NULL)
    uploadedBy = models.CharField(max_length=100)
    Factory = models.ForeignKey(Factory, null=True, on_delete=models.SET_NULL)
    Files=models.ManyToManyField(UploadedFile_S3,blank=True)
    def __str__(self):
        return self.programName


class ProgramAttachment(models.Model):
    Attachement = models.FileField(upload_to=program_directory_path, validators=[
                                   FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    awarenessProgram = models.ForeignKey(
        AwarenessProgram, on_delete=models.CASCADE, related_name='attachments')

    def __str__(self):
        return self.Attachement.name


def case_directory_path(instance, filename):
    return 'uploads/cases/cases_{0}/{1}'.format(instance.Date, filename)


# model for a complainer for a case will usually be a factory worker
class Complainer(models.Model):
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)
    Factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    PhoneNo = models.CharField(default="", max_length=15)
    Department = models.CharField(default="", blank=True, max_length=500)
    SubDepartment = models.CharField(default="", blank=True, max_length=500)
    Registered = models.BooleanField(default=False)
    Batch = models.CharField(default="", blank=True, max_length=500)
    is_active = models.BooleanField(default=True)
    Gender = models.CharField(
        choices=Gender.choices, default=Gender.NOT_SPECIFIED, max_length=15,
    )
    Language = models.CharField(
        choices=Language.choices, default=Language.English, max_length=20
    )

    def __str__(self):
        return str(self.PhoneNo) + " " + str(self.Factory)


class Case(models.Model):

    CaseNumber = models.CharField(
        max_length=50, unique=True, null=False, blank=True)

    Complainer = models.ForeignKey(
        Complainer, on_delete=models.CASCADE, null=True, blank=True)
    CallRecording_url = models.CharField(max_length=5000, default="")
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)
    Factory = models.ForeignKey(Factory, on_delete=models.CASCADE,)
    ReportingMedium = models.CharField(
        choices=ReportingMedium.choices,
        default=ReportingMedium.CALL,
        max_length=64
    )
    Date = models.DateTimeField(default=timezone.now, blank=True)
    Time = models.CharField(default=(timezone.now),
                            blank=True, max_length=500)
    CaseCategory = models.CharField(max_length=50, blank=True, null=True)
    SubCategory = models.CharField(max_length=50, blank=True, null=True)
    CaseValidation = models.BooleanField(default=True, null=True)
    CaseNature = models.CharField(
        choices=CaseNature.choices, default=CaseNature.COMPLAIN, max_length=64
    )
    CurrentStatus = models.CharField(
        choices=CaseActiveStatus.choices,
        default=CaseActiveStatus.NEW_CASE,
        max_length=20
    )
    Priority = models.CharField(max_length=200, blank=True, null=True)
    CaseReporter = models.ForeignKey(
        UserRoleFactory, on_delete=models.SET_NULL, related_name='cases_r', null=True, blank=True)
    CaseManager = models.ForeignKey(
        UserRoleFactory, on_delete=models.SET_NULL, related_name='cases_m', null=True, blank=True)
    CaseTroubleShooter = models.ForeignKey(
        UserRoleFactory, on_delete=models.SET_NULL, related_name='cases_t', null=True, blank=True)
    RegionalAdmin = models.ForeignKey(
        UserRoleFactory, on_delete=models.SET_NULL, related_name='cases_a', null=True, blank=True)
    CaseStatus = models.CharField (
        choices=CaseStatus.choices, 
        default=CaseStatus.ASSIGNED_TO_REPORTER,
        max_length=64
    )
    Counter = models.IntegerField(default=1, blank=True)
    CommentsByRep = models.CharField(max_length=5000, blank=True)
    CommentsByMan = models.CharField(max_length=5000, blank=True)
    # for incentive calculations
    T0 = models.IntegerField(default=0, blank=True)
    # for incentive calculations
    T1 = models.IntegerField(default=0, blank=True)
    # for incentive calculations
    T2 = models.IntegerField(default=0, blank=True)
    # for incentive calculations
    T3 = models.IntegerField(default=0, blank=True)
    T1vrfDate = models.DateTimeField(
        blank=True, null=True)  # for incentive calculations
    T2vrfDate = models.DateTimeField(
        blank=True, null=True)  # for incentive calculations
    T3vrfDate = models.DateTimeField(
        blank=True, null=True)  # for incentive calculations
    T0Breached = models.BooleanField(blank=True, null=True)
    T1Breached = models.BooleanField(blank=True, null=True)
    T2Breached = models.BooleanField(blank=True, null=True)
    T3Breached = models.BooleanField(blank=True, null=True)
    Breached = models.BooleanField(blank=True, null=True)
    t3a1 = models.BooleanField(blank=True, null=True)
    t3a2 = models.BooleanField(blank=True, null=True)
    t3b1 = models.BooleanField(blank=True, null=True)
    t3b2 = models.BooleanField(blank=True, null=True)
    t3c1 = models.BooleanField(blank=True, null=True)
    t3c2 = models.BooleanField(blank=True, null=True)
    reopened = models.BooleanField(default=False)
    ResolveTime = models.DateTimeField(blank=True, null=True)
    ClosingTime = models.DateTimeField(blank=True, null=True)
    CaseDetails = models.CharField(max_length=5000, blank=True,null=True)
    MessagebyWorker = models.CharField(max_length=5000,blank=True)
    workerLanguage = models.CharField(max_length=500,blank=True)
    File = models.ManyToManyField(UploadedFile_S3,blank=True)
    class Meta:
        permissions = (
            ("change_CaseDetails", "can change CaseDetails"),

        )

    def __str__(self):
        return str(self.CaseNumber + " -  " + str(self.id))
    

class Incentives(models.Model):
    Case = models.ForeignKey(Case, on_delete=models.CASCADE)
    #valid = models.BooleanField(default=True, null=True)
    CRsendDate = models.DateTimeField(blank=True, null=True)
    CRreceiveDate = models.DateTimeField(blank=True, null=True)
    CMsendDate = models.DateTimeField(blank=True, null=True)
    CMreceiveDate = models.DateTimeField(blank=True, null=True)
    CTsendDate = models.DateTimeField(blank=True, null=True)
    CTreceiveDate = models.DateTimeField(blank=True, null=True)


class CaseReslovingReport(models.Model):

    Case = models.OneToOneField(
        Case, on_delete=models.CASCADE, primary_key=True)
    CCRremarks = models.CharField(max_length=500, blank=True)
    CCRWhen = models.CharField(max_length=5000, blank=True)
    CCRWho = models.CharField(max_length=500, blank=True)
    CCRWhere = models.CharField(max_length=5000, blank=True)
    CCRWhathappened = models.CharField(max_length=5000, blank=True)
    CCTemplate = models.CharField(max_length=5000, blank=True)
    CCLanguage = models.CharField(max_length=20, blank=True)
    CCMessage = models.CharField(max_length=5000, blank=True)
    CCRvariables = models.JSONField(default=None, null=True)
    TimeToResolveCase = models.TimeField(default=timezone.now, blank=True)
    CCRComments_RA=models.CharField(max_length=5000, blank=True,default="",null=True)

    def __str__(self):
        return str(self.Case)


class BroadcastMessage(models.Model):
    lastModified = models.DateTimeField(default=timezone.localtime, blank=True)
    createdBy = models.CharField(max_length=100)
    Languages = ArrayField(models.CharField(max_length=100), default=list)
    templateTitle = models.CharField(max_length=100)
    sendCount = models.IntegerField()
    status = models.CharField(
        choices=Status.choices, default=Status.SENT, max_length=15,
    )
    Genders = ArrayField(models.CharField(max_length=1000), default=list)
    templateIDs = ArrayField(models.CharField(max_length=1000), default=list)
    departments = ArrayField(models.CharField(max_length=1000), default=list,null=True,blank=True)
    Departments = models.JSONField(default=None, null=True)
    messageBody = ArrayField(models.JSONField(max_length=1000), default=list)
    # sendFilter = ArrayField(models.JSONField(max_length=1000), default=list)
    inputVariables = models.JSONField(default=None, null=True)
    Factory = models.ForeignKey(
        Factory,
        on_delete=models.CASCADE, null=True
    )
    Company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE, null=True
    ) 
    factories = ArrayField(models.CharField(max_length=1000), default=list)


# model for reopening the case, its object is made when a case is reopened
class ReopenCase(models.Model):
    Case = models.ForeignKey(Case, on_delete=models.CASCADE)
    TOC = models.CharField(max_length=5000, blank=True)
    IC = models.CharField(max_length=5000, blank=True)
    QOE = models.CharField(max_length=5000, blank=True)
    Remarks = models.CharField(max_length=50000, blank=True)


# model for keepinf logs for data comig from tatawebhooks
class TatawebhooksLog(models.Model):
    receivedAt = models.DateTimeField(
        help_text="when webhook accesses our url")
    payload = models.JSONField(default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["receivedAt"]),
        ]


class SMSTemplates(models.Model):

    templateID = models.CharField(max_length=500)

    body = models.CharField(max_length=5000)
    Title = models.CharField(max_length=5000, blank=True)
    language = models.CharField(
        choices=Language.choices, default=Language.English, max_length=100
    )
    Company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True)
    variables = models.JSONField(default=None, null=True)
    template_categories = ArrayField(
        models.CharField(max_length=1000), default=list)
    user_roles_access = ArrayField(
        models.CharField(max_length=1000), default=list
    )

    def __str__(self):
        return self.templateID + " " + self.Title + " " + self.language


class AuditLog(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE,null=True, blank=True)
    status = models.CharField(choices=CaseStatus.choices, max_length=64)
    created_at = models.CharField(
        default=(timezone.localtime), blank=True, max_length=500)
    created_by = models.ForeignKey(
        UserRoleFactory, on_delete=models.CASCADE, related_name="cretbyal",null=True)
    
    # modified_by= models.ForeignKey(BaseUserModel,on_delete=models.CASCADE,null=True)
    # modified_at = models.DateTimeField(default=timezone.now)
    var_changed = models.CharField(max_length=64)
    prev_state = models.CharField(max_length=64, null=True)
    current_state = models.CharField(max_length=64)
    message = models.CharField(max_length=5000)
    action_type = models.CharField(max_length=80)
    error_message = models.CharField(max_length=100, blank=True)
    # uploaded_by = models.ForeignKey(UserRoleFactory, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return str(self.case) + " " + self.action_type


class HolidayCalendar(models.Model):
    eventName = models.CharField(max_length=30)
    startDate = models.DateTimeField(null=True, blank=True)
    endDate = models.DateTimeField(null=True, blank=True)
    Factory = models.ForeignKey(
        Factory,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.eventName


class scheduleInformation(models.Model):
    Information = models.JSONField()
    type = models.CharField(
        choices=scheduleType.choices,
        default=scheduleType.SEND_MESSAGE,
        max_length=100
    )
    is_active = models.BooleanField(default=True)
    count = models.IntegerField(default=0)
class SNSTemplate(models.Model):
    template_id = models.CharField(max_length=255,null=True)
    body = models.TextField()
    subject = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=255)  # Assuming language is a single value, you can adjust if it's a list
    variables = models.JSONField(default=None,null=True)
    template_category = models.CharField(max_length=255)
    company_fk = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.template_id} - {self.title}" 
class Notification(models.Model):
    subscription_to_be_triggered = models.CharField(max_length=50)
    notification_rules = models.JSONField(default=None, null=True)
    schedule = models.CharField(max_length=255)
    template_fk = models.ForeignKey(SNSTemplate, on_delete=models.SET_NULL,null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=255)
    title=models.CharField(max_length=500)
    event_identifier_items = models.JSONField( blank=True, null=True)

    def __str__(self):
        return f"{self.subscription_to_be_triggered} - {self.title}"

class NotificationLog(models.Model):
    notification_fk = models.ForeignKey(Notification, on_delete=models.SET_NULL,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message_subject = models.CharField(max_length=1000)
    message_content = models.CharField(max_length=10000)
    template_fk = models.ForeignKey(SNSTemplate, on_delete=models.SET_NULL,null=True)
    sns_topic_name = models.CharField(max_length=1000)
    notification_type = models.CharField(max_length=255)
    log = models.JSONField(default=None, null=True)
    event_identifier = models.JSONField( blank=True, null=True)


    def __str__(self):
        return f"{self.notification_fk} - {self.timestamp}"
    

class IncentivePermission(models.Model):
    class Meta:
        managed = False 
        permissions = (
            ('view_incentives', 'Can view incentives'),
        )
        app_label = 'accounts'



@receiver(pre_save, sender=Case)
def if_priority_changed(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Object is new, so field hasn't technically changed, but you may want to do something else here.
        pass
    else:
        # priority has changed from obj.priority to instance.priority
        
        if not obj.Priority == instance.Priority:  # Field has changed
            # caselogs = CaseLogs.objects.create(Case=obj, priority=instance.Priority)
            if instance.Priority == None:
                instance.Priority = ""
            user = getuser(obj)
            auditlog = AuditLog.objects.create(
                case=obj,
                status=obj.CaseStatus,
                created_by=user,
                var_changed="Priority",
                prev_state=obj.Priority,
                current_state=instance.Priority,
                action_type=ActionTypes.PRIORITY_PUT
            )


@receiver(pre_save, sender=Case)
def if_validity_changed(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Object is new, so field hasn't technically changed, but you may want to do something else here.
        pass
    else:
        # priority has changed from obj.priority to instance.priority
        if not obj.CaseValidation == instance.CaseValidation:  # Field has changed
            # caselogs = CaseLogs.objects.create(Case=obj, priority=instance.Priority)
            user = getuser(obj)
            auditlog = AuditLog.objects.create(
                case=obj,
                status=obj.CaseStatus,
                created_by=user,
                var_changed="CaseValidation",
                prev_state=obj.CaseValidation,
                current_state=instance.CaseValidation,
                action_type=ActionTypes.CASEVALIDATION_PUT,
            )


@receiver(pre_save, sender=Case)
def if_nature_changed(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Object is new, so field hasn't technically changed, but you may want to do something else here.
        pass
    else:
        # priority has changed from obj.priority to instance.priority
        if not obj.CaseNature == instance.CaseNature:  # Field has changed
            # caselogs = CaseLogs.objects.create(Case=obj, priority=instance.Priority)
            user = getuser(obj)
            auditlog = AuditLog.objects.create(
                case=obj,
                status=obj.CaseStatus,
                created_by=user,
                var_changed="CaseNature",
                prev_state=obj.CaseNature,
                current_state=instance.CaseNature,
                action_type=ActionTypes.CASEVALIDATION_PUT,
            )


def if_CaseFileupload_changed(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Object is new, so field hasn't technically changed, but you may want to do something else here.
        pass
    else:
        # priority has changed from obj.priority to instance.priority
        if not obj.CaseFileupload == instance.CaseFileupload:  # Field has changed
            # caselogs = CaseLogs.objects.create(Case=obj, priority=instance.Priority)
            user = getuser(obj)
            auditlog = AuditLog.objects.create(
                case=obj,
                status=obj.CaseStatus,
                created_by=user,
                var_changed="Document",
                prev_state=obj.CaseFileupload,
                current_state=instance.CaseFileupload,
                action_type=ActionTypes.CASEFILE_PUT,
            )


@receiver(pre_save, sender=Case)
def if_category_changed(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if not obj.CaseCategory == instance.CaseCategory:
            # caselogs = CaseLogs.objects.create(Case=obj, Category=instance.CaseCategory)
            user = getuser(obj)
            auditlog = AuditLog.objects.create(
                case=obj,
                status=obj.CaseStatus,
                created_by=user,
                var_changed="CATEGORY",
                prev_state=obj.CaseCategory,
                current_state=instance.CaseCategory,
                action_type=ActionTypes.CATEGORY_PUT,
            )


@receiver(pre_save, sender=Case)
def if_subcategory_changed(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if not obj.SubCategory == instance.SubCategory:
            # caselogs = CaseLogs.objects.create(Case=obj, SubCat=instance.SubCategory)
            user = getuser(obj)
            auditlog = AuditLog.objects.create(
                case=obj,
                status=obj.CaseStatus,
                created_by=user,
                var_changed="SUBCATEGORY",
                prev_state=obj.SubCategory,
                current_state=instance.SubCategory,
                action_type=ActionTypes.SUBCATEGORY_PUT,
            )


@receiver(pre_save, sender=Case)
def if_status_changed(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass
    else:
        if not obj.CaseStatus == instance.CaseStatus:
            # caselogs = CaseLogs.objects.create(Case=obj, SubCat=instance.CaseStatus)
            user = getuser(obj)
            auditlog = AuditLog.objects.create(
                case=obj,
                status=obj.CaseStatus,
                created_by=user,
                var_changed="CaseStatus",
                prev_state=obj.CaseStatus,
                current_state=instance.CaseStatus,
                action_type=ActionTypes.STATUS_PUT,
            )


# @receiver(pre_save, sender=Case)
# def if_CR_updated(sender, instance, **kwargs):
#     try:
#         obj = sender.objects.get(pk=instance.pk)
#     except sender.DoesNotExist:
#         pass
#     else:
#         if not obj.CaseReporter == instance.CaseReporter:
#             # caselogs = CaseLogs.objects.create(Case=obj, SubCat=instance.CaseStatus)
#             user = getuser(obj)
#             # print(user)
#             auditlog = AuditLog.objects.create(
#                 case=obj,
#                 status=obj.CaseStatus,
#                 created_by=instance.CaseReporter,
#                 var_changed=" CaseReporter",
#                 prev_state=obj.CaseReporter,
#                 current_state=instance.CaseReporter,
#                 action_type=ActionTypes.CR_PUT
#             )


# @receiver(pre_save, sender=Case)
# def if_CM_updated(sender, instance, **kwargs):
#     try:
#         obj = sender.objects.get(pk=instance.pk)
#     except sender.DoesNotExist:
#         pass
#     else:
#         if not obj.CaseManager == instance.CaseManager:
#             caselogs=CaseLogs.objects.create(Case=obj, SubCat=instance.CaseStatus)
#             user=getuser(obj)
#             print(user)
#             auditlog=AuditLog.objects.create(case=obj,status=obj.CaseStatus,created_by=user,var_changed="CaseManager",prev_state=obj.CaseManager,current_state=instance.CaseManager,message="CaseManager Updated",action_type="PUT")
#             print(obj.CaseManager,instance.CaseManager)
# @receiver(pre_save, sender=Case)
# def if_CT_updated(sender, instance, **kwargs):
#     try:
#         obj = sender.objects.get(pk=instance.pk)
#     except sender.DoesNotExist:
#         pass
#     else:
#         if not obj.CaseTroubleShooter == instance.CaseTroubleShooter:
#             caselogs=CaseLogs.objects.create(Case=obj, SubCat=instance.CaseStatus)
#             user=getuser(obj)
#             print(user)
#             auditlog=AuditLog.objects.create(case_id=obj,status=obj.CaseStatus,created_by=user,var_changed="CaseTroubleShooter",prev_state=obj.CaseTroubleShooter,current_state=instance.CaseTroubleShooter,message="CaseTroubleShooter Updated",action_type="PUT")
#             print(obj.CaseTroubleShooter,instance.CaseTroubleShooter)


def getuser(obj):
    if obj.CaseStatus == CaseStatus.ASSIGNED_TO_REPORTER:
        return obj.CaseReporter
    elif obj.CaseStatus == CaseStatus.ASSIGNED_TO_MANAGER:
        return obj.CaseManager
    elif (
        obj.CaseStatus == CaseStatus.ASSIGNED_TO_TROUBLESHOOTER
        or obj.CaseStatus == CaseStatus.UNDER_INVESTIGATION
        or obj.CaseStatus == CaseStatus.RESOLVED
        or obj.CaseStatus == CaseStatus.RE_INVESTIGATION
    ):
        return obj.CaseTroubleShooter


@receiver(post_save, sender=Case)
def create_incentives(sender, instance, created, **kwargs):
    if created:
        Incentives.objects.create(Case=instance)
