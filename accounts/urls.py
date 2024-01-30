from accounts.Utils.NotificationUtil.EmailTemplateImport import importawstemplates
from accounts.controller.UpdateController import FileDirectUploadApi
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .controller.CaseController import CaseCloseAV, CaseDetailsAV, Cases, sanitiseCaseNature
from .controller.awarenessController import ProgramDetails, calendarCheck
from .controller.holidayController import HolidayDetails, bulkHolidayUpload, downloadHoliday, bulkUploadCSV
from .controller.regionController import RegionDetails, sanitiseRegions, fetchFactories
from accounts.factoryviews import FactoryAV, factoryCodesUpdate
from accounts.userviews import UserAV, addAssignUserRoleAV, userInformation, sanitiseNames, sanitiseInactiveUsers, sanitiseIncentivePerms, disableFAs, sanitisePoshSpecialCases
from accounts.incentives import winner
from accounts.broadcastViews import TemplateDetails, departmentlist, BroadcastMessageAV, FilterTemplates, BroadcastDraft, EditDraft, VariableMapping, sanitizebroadcastmessages
from accounts.uploads import masterDataUpload
from accounts.analytics import (
    uploadMetrics, 
    getAllMetrics, 
    getEmailMetrics, 
    getUserMetric, 
    uploadUserMetrics, 
    getTableMetrics, 
    getMetric,
    createMetricTables,
    deleteTableMetrics,
    getActiveUserMetrics,
    getAverageSessionDuration,
    getAveragePages,
    getBounceRate,
    getRoleLogins,
    getUserRetention,
    getChurnRate,
    export_analytics_to_csv
)
from accounts.views import (
    AssignCaseAV,
    # BUMDetailsAV,
    # BUMList,
    CCReportDetailsAV,
    gender_sanitize_api,
    patchRA,
    CaseSLAReopenAV,
    CaseFilter,
    # CaseManDetailsAV,
    CaseManListAV,
    # CaseRepDetailsAV,
    CaseRepListAV,
    CaseResolveAV,
    CaseTotalAV,
    # CaseTrbDetailsAV,
    CaseTrbListAV,
    CaseUploadAV,
    CompanyDetailsAV,
    CompanyListAV,
    ComplainerViewSet,
    CustomTokenObtainPairView,
    FacFilter,
    GetSmstemplates,
    PasswordTokenCheckAV,
    QCCaseReopenAV,
    QCNewCaseListAV,
    sanitizeRA,
    ReportIncntvView,
    RequestPasswordResetEmailAV,
    RoleListAV,
    SetNewPasswordAV,
    WinnerView,
    CaseSendMessageKlyra,
    encodeID,
    logout_view,
    importtemplate,
    CaseCountView,
    CaseCreatorFileAV,
    FactoryDetailsAV,
    CaseCallwebhook,
    CaseSepCount,
    ViewLogsAV,
    sanitiseCases,
    DepartmentUpload,
    CTMessageDraft,
    sanitiseUserPermissions,
    sanitizeCases,
    sanitizeRoles,
    sanitiseIncentives,
    sanitizeprofilepics,
    sanitizerinactiveoles,
    sanitizeSA,
    sanitizeBaseUsers,
    sanitizeuserpermissions,
    sanitizecasevalidations,
    sns_webhook,
    unsubscribe_view
)

from rest_framework import routers
from accounts.views import ComplainerViewSet
from django.urls import path, include, re_path
from accounts.uploads import getLanguages

router = routers.DefaultRouter()
router.register(r'complainers', ComplainerViewSet, basename='complainers')
urlpatterns = [
    path('', include(router.urls)),

    path(
        "api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # login endpoint
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # refresh token endpoint
    # path(
    #     "baseusers/", BUMList.as_view(), name="getbaseusers"
    # ),  # returns list of all the users
    # path(
    #     "baseuser/<int:pk>", BUMDetailsAV.as_view()
    # ),  # RETURNS THE DETAILS OF A PARTICULAR USER

    # returns list of all the companys
    path("companys/", CompanyListAV.as_view()),
    path(
        "company/<int:pk>/", CompanyDetailsAV.as_view()
    ),  # returns the details for aparticular company
    path("logout/", logout_view, name="logout"),  # logout endpoint
    # path(
    #     "company/<str:c>/factory-create/", CompanyFactoryPost.as_view()
    # ),  # endpoint to create a factory for a company
    # returns list of all the factories for a particular company
    path(
        "factory/<int:pk>", FactoryDetailsAV.as_view()
    ),  # returns the details of a factory
    path(
        "company/<str:c>/factory/<str:f>/caserep", CaseRepListAV.as_view()
    ),  # returns list of all the casereporters for a company and a factory
    path(
        "company/<str:c>/factory/<str:f>/caseman", CaseManListAV.as_view()
    ),  # returns list of all the casemanagers for a company and a factory
    path(
        "company/<str:c>/factory/<str:f>/casetrb", CaseTrbListAV.as_view()
    ),  # returns list of all the casetroubleshooters for a company and a factory
    path("company/<str:companyId>/factory/<str:factoryId>/cases/", Cases.as_view()),
    path(
        "company/<str:c>/factory/<str:f>/qc/newcases/", QCNewCaseListAV.as_view()
    ),  # returns the list of all the new and unread cases for a qc
    path(
        "dept/upload/", DepartmentUpload
    ),  # endpoint to upload master data for a company
    path(
        "case/upload/", CaseUploadAV
    ),  # endpoint to upload a case for in person complaints
    path(
        "CaseswithFileUpload/", CaseCreatorFileAV.as_view()
    ),  # endpoint to create a case with file upload for suggestion box etc.
    # path(
    #     "CaseRep/<int:pk>", CaseRepDetailsAV.as_view()
    # ),  # returns the details of a casereporter
    # path(
    #     "CaseTrb/<int:pk>", CaseTrbDetailsAV.as_view()
    # ),  # returns the details of a casetroubleshooter
    # path(
    #     "CaseMan/<int:pk>", CaseManDetailsAV.as_view()
    # ),  # returns the details of a casemanager
    path(
        "Cases/<int:caseId>", CaseDetailsAV.as_view()
    ),  # returns the details of a particular case
    path(
        "case/resolve/", CaseResolveAV.as_view()
    ),  # Case closing report upload endpoint
    # endpoint to resolve a case
    path("case/<int:pk>/close/", CaseCloseAV.as_view()),

    path(
        "Case/<int:pk>/CCreport/", CCReportDetailsAV.as_view()
    ),  # returns the CCR for a particular case
    path("Case/qc/reopen/", QCCaseReopenAV),  # endpoint to reopen a case
    path(
        "Case/ct/reopen/sla/", CaseSLAReopenAV.as_view()
    ),  # endpoint to reopen a case
    path(
        "cases/total/", CaseTotalAV.as_view()
    ),  # returns the total number of cases for a particular company
    # returns all the incentives data
    path("cases/sepcount", CaseSepCount.as_view()),
    path("cases/fil", FacFilter.as_view()),  # analytics data including filters
    # permissions done till here
    path(
        "caseCount/", CaseCountView.as_view()
    ),  # returns the count of cases for a particular company
    # path('caseMessager/', CaseMessagerView.as_view()),  #returns the list of all the messages for a particular case')
    path("report/incntv/", ReportIncntvView.as_view()),
    path(
        "winner/", WinnerView.as_view()
    ),  # returns the list of all the winners for a particular company')
    path(
        "tata/webhook/case/call/", CaseCallwebhook, name="case_call_webhook"
    ),  # endpoint to handle the webhooks for the case call
    path(
        "sns/", sns_webhook,),  # endpoint to handle the webhooks for the case call
    path(
        "klrya/temp/update/", importtemplate, name="temp_update"
    ),  # Endpoint to upload sms templates
    path("case/sendmsg/", CaseSendMessageKlyra.as_view()),  # endpoint tosend sms
    # endpoint to close a case
    # path("case/<int:pk>/close/", CaseCloseAV.as_view()),
    path(
        "request-reset-email/",
        RequestPasswordResetEmailAV.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset/<str:uidb64>/<str:token>/",
        PasswordTokenCheckAV.as_view(),
        name="password_reset_confirm",
    ),  # endpoint to reset the password
    path(
        "password-reset-complete/",
        SetNewPasswordAV.as_view(),
        name="password_reset_complete",
    ),  # endpoint to complete the password reset
    path(
        "gettemps/", GetSmstemplates.as_view()
    ),  # endpoint to get sms templates fromthe backend
    path("template/", TemplateDetails.as_view()),
    path("varmap/", VariableMapping.as_view()),
    path("broadcast/", BroadcastMessageAV.as_view()),
    path("filtermsgs/", FilterTemplates.as_view()),
    path("savedraft/", BroadcastDraft.as_view()),
    path("ctdraft/", CTMessageDraft.as_view()),
    # TODO
    # path("filledtmps/", SessionTemplates.as_view()), # url to store user filled templates temporarily in a session
    path("draftstatus/", EditDraft.as_view()),

    path("cleancases/", sanitiseCases),
    path("logs/", ViewLogsAV.as_view()),

    path("template/", TemplateDetails.as_view()),
    path("users/", UserAV.as_view()),
    # returns list of all available roles
    path("roles/", RoleListAV.as_view()),
    # api to assign cases from one user to other
    path("assign-cases/", AssignCaseAV.as_view()),
    # case filter for factory and company
    path("cases/", CaseFilter.as_view()),
    # user filter for factory and company
    path(
        "factories/", FactoryAV.as_view()
    ),  # GET POST PUT DELETE for factories
    path(
        "userInput/", userInformation.as_view()
    ),
    path("awareness/",ProgramDetails.as_view()),
    path("check/",calendarCheck),
    path('upload/', FileDirectUploadApi.as_view()),
    path("bulkholidayupload/",bulkHolidayUpload),
    path("holiday/",HolidayDetails.as_view()),
    path("downloadPDF/",downloadHoliday),
    path("sanitizeuserperms/",sanitiseUserPermissions),
    path("sampleCSV/",bulkUploadCSV),
    path('sanitizeroles/',sanitizeRoles),
    path('sanitizeCases/',sanitizeCases),
    path('sanitizerinactiveoles/',sanitizerinactiveoles),
    path('encode/',encodeID),
    path("cleanIncentives/", sanitiseIncentives),
    path("winnerIncentives/",winner),
    path("getLanguages/",getLanguages),
    path("add-assign/",addAssignUserRoleAV.as_view()),
    path('sanitiseCaseNature/',sanitiseCaseNature),
    path('sanitizeprofilepics/',sanitizeprofilepics),
    path('sanitiseNames/',sanitiseNames),
    path("region/",RegionDetails.as_view()),
    path("cleanRegions/", sanitiseRegions),
    path("fetchFactories/", fetchFactories),
    path("sanitiseRA/", sanitizeRA),
    path("patchRA/", patchRA),
    path("departments/", departmentlist),
    path("sanitiseMsgs/", sanitizebroadcastmessages),
    path("sanitiseSA/", sanitizeSA),
    path("sanitiseBaseUsers/", sanitizeBaseUsers),
    path("sanitiseperms/", sanitizeuserpermissions),
    path("gendersanitize/", gender_sanitize_api),
    path('sanitisecasevalidations/',sanitizecasevalidations),
    path('sanitiseInactiveUsers/',sanitiseInactiveUsers),
    path('updateFactoryCodes/',factoryCodesUpdate),
    path('sanitiseIncentivePerms/',sanitiseIncentivePerms),
    path('disableFAs/',disableFAs),
    path('workerDataUpload/',masterDataUpload),
    path('sanitisePoshSpecialCases/',sanitisePoshSpecialCases),
    #Single Table Approach API's
    path('uploadMetrics/',uploadMetrics),
    path('getAllMetrics/',getAllMetrics),
    path('getEmailMetrics/',getEmailMetrics),
    path('getUserMetrics/',getUserMetric),
    #Multiple Table Approach API's
    path('uploadUserMetrics/',uploadUserMetrics),
    path('getTableMetrics/',getTableMetrics),
    path('getMetric/',getMetric),
    path('createMetricTables/',createMetricTables),
    path('deleteTableMetrics/',deleteTableMetrics),
    path('getActiveUserMetrics/',getActiveUserMetrics),
    path('getAverageSessionDuration/',getAverageSessionDuration),
    path('getAveragePages/',getAveragePages),
    path('getBounceRate/',getBounceRate),
    path('getRoleLogins/',getRoleLogins),
    path('getUserRetention/',getUserRetention),
    path('getChurnRate/',getChurnRate),
    path('getAnalyticsCSV/',export_analytics_to_csv),
    path('importawstemplates/',importawstemplates),
    path('unsubscribe/<str:token>/', unsubscribe_view, name='unsubscribe'),

]
