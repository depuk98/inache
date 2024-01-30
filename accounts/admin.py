from accounts.models import (
    AuditLog,
    AwarenessProgram,
    Notification,
    NotificationLog,
    Role,
    SMSTemplates,
    BaseUserModel,
    CaseReslovingReport,
    HolidayCalendar,
    Company,
    Complainer,
    Factory,
    Case,
    ReopenCase,
    SNSTemplate,
    TatawebhooksLog,
    UploadedFile_S3,
    User_Profilepic,
    UserRoleFactory,
    FactoryRegion
)
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator
from django.core.cache import cache


class CustomFilter(admin.SimpleListFilter):
    title = _('Custom Filter')  
    parameter_name = 'custom_filter' 

    def lookups(self, request, model_admin):
        return [
            ('option_one', _('All Shahi Factories except T27')),
        ]

    def queryset(self, request, queryset):

        if self.value() == 'option_one':
            return queryset.filter(Company=2).exclude(Factory=2)

class CaseAdmin(admin.ModelAdmin):
    model = Case
    list_select_related = ('Complainer', 'Company', 'Factory', 'CaseReporter', 'CaseManager', 'CaseTroubleShooter', 'RegionalAdmin')
    list_prefetch_related = ('File',)  # Add more related fields to prefetch if needed
    list_per_page = 25  # Adjust the number of records per page
    list_display = ('CaseNumber', 'Complainer', 'Company', 'Date', 'Factory', 'ReportingMedium', 'Time','CaseCategory', 'SubCategory', 'CaseValidation', 'CaseNature', 'CaseStatus',)  # Customize the fields displayed in the list view
    raw_id_fields = ('Complainer', 'Company', 'Factory', 'CaseReporter', 'CaseManager', 'CaseTroubleShooter', 'RegionalAdmin')  # Add the fields that you want to be displayed as a raw id field
    fieldsets = (
        ('Basic Information', {
            'fields': ('CaseNumber', 'Complainer', 'Company', 'Factory', 'ReportingMedium', 'Date', 'Time'),
        }),
        ('Case Details', {
            'fields': ('CaseCategory', 'SubCategory', 'CaseValidation', 'CaseNature', 'CurrentStatus', 'Priority', 'CaseStatus', 'CaseReporter', 'CaseManager', 'CaseTroubleShooter', 'RegionalAdmin','CommentsByRep','CommentsByMan'),
        }),
        ('Incentive Details', {
            'fields': ('T0', 'T1', 'T2', 'T3', 'T1vrfDate', 'T2vrfDate', 'T3vrfDate', 'T0Breached', 'T1Breached', 'T2Breached', 'T3Breached', 'Breached','t3a1', 't3a2', 't3b1', 't3b2', 't3c1', 't3c2'),
        }),
        ('Other Details', {
            'fields': ( 'reopened', 'ResolveTime', 'ClosingTime', 'CaseDetails', 'MessagebyWorker', 'workerLanguage', 'File'),
        }),
    )
    list_filter = ('Company', 'Factory', CustomFilter,)
    
    
admin.site.register(BaseUserModel)
admin.site.register(AwarenessProgram)
admin.site.register(User_Profilepic)
admin.site.register(Factory)
admin.site.register(FactoryRegion)
admin.site.register(UploadedFile_S3)
admin.site.register(Company)
admin.site.register(Case,CaseAdmin)
admin.site.register(Complainer)
admin.site.register(CaseReslovingReport)
admin.site.register(ReopenCase)
admin.site.register(TatawebhooksLog)
admin.site.register(AuditLog)
admin.site.register(SMSTemplates)
admin.site.register(HolidayCalendar)
admin.site.register(Permission)
admin.site.register(UserRoleFactory)
admin.site.register(NotificationLog)
admin.site.register(SNSTemplate)
admin.site.register(Notification)
