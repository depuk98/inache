from rest_framework.request import Request
from InacheBackend import settings
from accounts.Service.CMService import assign_cm
from accounts.Service.CTService import assign_ct
from accounts.Service.RAService import assign_ra
from accounts.Service.CasesService import CasesService
from accounts.constants import ActionTypes, CaseActiveStatus, CaseStatus, UserRole, CaseNature
from accounts.errors import serialer_error
from accounts.models import AuditLog, Case, UserRoleFactory
from accounts.permissions import HasGroupPermission, is_same_company_user
from accounts.serializers import CaseRequestSerializerCM, CaseRequestSerializerCR, CaseSerializers
from accounts.Utils.userRoleParser import parser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import PermissionRequiredMixin
from drf_yasg.utils import swagger_auto_schema
from rest_framework import  status
from drf_yasg import openapi
import jwt
import datetime
from accounts.views import caseClosingMessage, sendCategoryMessage
from rest_framework.decorators import api_view
from accounts.utils import current_time
class Cases(APIView):
    # serializer_class = CaseSerializers
    permission_classes = [HasGroupPermission,is_same_company_user]
    required_groups = {
    'GET': ['CT','CR','CM','FACTORY_ADMIN','SUPER_ADMIN','REGIONAL_ADMIN'],
    }
    model = "case"

    # @api_view(['GET'])
    def get(self, request:Request, **kwargs:any)->Response:
        company_id = kwargs['companyId']
        factory_id = kwargs['factoryId']
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        # userRole=UserRoleFactory.objects.get(id=role_id.id)
        
        case_type = request.query_params.get("case_type")
        critical = request.query_params.get("critical")
        if case_type is None:
            return Response({"error": "Case type not specified."}, status=status.HTTP_400_BAD_REQUEST)
        cases_service = CasesService(company_id, factory_id)
        cases=cases_service.getCases(userRole.id, userRole.role.role,case_type, critical)
        # print(len(cases))
        if len(cases)==0:
            return Response([], status=status.HTTP_200_OK)
        # cases=cases.all().update(CurrentStatus=CaseActiveStatus.NEW_CASE)
        # print((cases),"dsadsadsa")
        # serializer=CaseSerializers(cases,many=True)
        return Response(cases)


class CaseDetailsAV(APIView, PermissionRequiredMixin):
   
    permission_classes = [
        # HasGroupPermission,is_same_company_user
        ]
    required_groups = {
        'GET': ['CR','CM','CT','FACTORY_ADMIN','SUPER_ADMIN','REGIONAL_ADMIN'],
        'PUT': ['CR','CM','CT','REGIONAL_ADMIN' ],
    }
    model = "case"
    # http_method_names = ['get_case']

    @swagger_auto_schema(responses={
        200: openapi.Response('Successful response', CaseSerializers),
        400: 'Invalid request',
        404: 'Case not found'
    })
    def get(self,request:Request, caseId:int)->Response:
        try:
            userRole=parser(request)
            if userRole is None:
                return Response({"error":"ROLE ID NOT PRESENT"})
            # userRole=UserRoleFactory.objects.get(id=167)
            case_result = Case.objects.get(pk=caseId)
            serializer = CaseSerializers(case_result)
            data = dict(serializer.data)
            # Updating the status from unread to read
            if(case_result.CurrentStatus!=CaseActiveStatus.DRAFT):
                query_params = {
                    UserRole.CASE_REPORTER: 
                        [CaseStatus.ASSIGNED_TO_REPORTER]
                    ,
                    UserRole.CASE_MANAGER: 
                        [CaseStatus.ASSIGNED_TO_MANAGER]
                        ,
                    UserRole.CASE_TROUBLESHOOTER: 
                            CaseStatus.ASSIGNED_TO_TROUBLESHOOTER 
                        ,
                    UserRole.SUPER_ADMIN: 
                            ""
                        ,
                    UserRole.FACTORY_ADMIN: 
                            ""
                        ,
                    UserRole.REGIONAL_ADMIN: 
                            CaseStatus.ASSIGNED_TO_REGIONAL_ADMIN 
                        ,
                }
                casestatus=query_params.get(userRole.role.role)
                if( case_result.CaseStatus in casestatus ):
                    Case.objects.filter(pk=caseId).update(CurrentStatus=CaseActiveStatus.READ)
            return Response((data))
        except Case.DoesNotExist:
            return Response({'Error': "Case Not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=CaseSerializers)
    def put(self,request:Request, caseId:int)->Response:
        case = Case.objects.get(pk=caseId)
        # print(case.SubCategory)
        serializer = CaseSerializers(case, data=request.data)
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        if serializer.is_valid():
            if request.data['CurrentStatus']!= CaseActiveStatus.DRAFT:
                
                if userRole.role.role==UserRole.CASE_REPORTER:
                    request_serializer =CaseRequestSerializerCR(data=request.data)
                    if request_serializer.is_valid():
                        if request.data.get('CaseCategory') == "POSH" or request.data.get('CaseCategory') == "Special Cases":
                            if case.Complainer:
                                regional_admin = request.data.get('RegionalAdmin')
                                if (regional_admin is None) or (regional_admin == ""):
                                    return Response({'Error': "Regional Admin is required"}, status=status.HTTP_400_BAD_REQUEST) 
                                response,response_status=assign_ra(request,caseId)
                            else:
                                return Response({"errorMessage":"Categories with POSH or SPECIAL CASES need Complainer Number to Procees"},status=status.HTTP_400_BAD_REQUEST)
                        else:
                            case_manager= request.data.get('CaseManager')
                            if (case_manager is None) and (request.data.get('CaseValidation')==True):
                                return Response({'Error': "Case Manager is required"}, status=status.HTTP_400_BAD_REQUEST) 
                            response,response_status=assign_cm(request,case_manager,caseId)
                        if response is None:
                            return Response({"error":"ROLE ID NOT PRESENT"},status=status.HTTP_404_NOT_FOUND)
                            
                        
                        return Response(response,response_status)
                    else:
                        error_response=serialer_error(request_serializer.errors)
                        # print(error_response)
                        return Response(
                                error_response
                            ,status=status.HTTP_400_BAD_REQUEST)
                elif userRole.role.role==UserRole.CASE_MANAGER:
                    request_serializer =CaseRequestSerializerCM(data=request.data)
                    if request_serializer.is_valid():
                        case_trb= request.data.get('CaseTroubleShooter')
                        if case_trb is None:
                            return Response({'Error': "CaseTroubleShooter is required"}, status=status.HTTP_400_BAD_REQUEST)
                        response,response_status=assign_ct(request,case_trb,caseId)
                        if response is None:
                            return Response({"error":"ROLE ID NOT PRESENT"},status=status)
                        return Response(response,response_status)
                    else:
                        error_response=serialer_error(request_serializer.errors)
                        return Response(
                                error_response
                            ,status=status.HTTP_400_BAD_REQUEST)
                elif userRole.role.role==UserRole.CASE_TROUBLESHOOTER:
                    pass
                elif userRole.role.role==UserRole.REGIONAL_ADMIN:
                    pass
            serializer.save()
            return Response(serializer.data)
        else:
            error_response=serialer_error(serializer.errors)
            # print(error_response)
            return Response(
                                error_response
                            ,status=status.HTTP_400_BAD_REQUEST)
            
            
class CaseCloseAV(APIView):
    permission_classes=[HasGroupPermission]
    required_groups = {
        'PUT': ['CR','CT','REGIONAL_ADMIN'],
    }
    model = "case"
    @swagger_auto_schema(request_body=CaseSerializers)
    def put(self, request, pk):
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        case1 = Case.objects.get(id=pk)
        data = request.data
        data["Counter"] = 6
        data["CaseStatus"] = CaseStatus.CLOSED
        data["ClosingTime"] = current_time()
        data["Company"] = case1.Company.id
        data["Factory"] = case1.Factory.id
        serializer = CaseSerializers(case1, data=data)
        # newstate = case1.save()
        if serializer.is_valid():
            newstate = serializer.save()
            if userRole.role.role == UserRole.CASE_REPORTER:
                newstate.CaseCategory = "Invalid"
                newstate.CaseValidation = False
                newstate.save()
                auditlog = AuditLog.objects.create(
                    case=case1,
                    status=case1.CaseStatus,
                    created_by=userRole,
                    var_changed="CaseStatus",
                    prev_state=case1.CaseStatus,
                    current_state=newstate.CaseStatus,
                    action_type=ActionTypes.CASE_INVALID,
                )
                if case1.Complainer:
                    body = sendCategoryMessage(case1,"invalid Message")
                    auditlog = AuditLog.objects.create(
                    case=case1,
                    status=case1.CaseStatus,
                    created_by=userRole,
                    prev_state="",
                    current_state="",
                    message=body,
                    action_type=ActionTypes.UNCLEAR_MESSAGE_SENT,
                )
                
            else:
                auditlog = AuditLog.objects.create(
                    case=case1,
                    status=case1.CaseStatus,
                    created_by=userRole,
                    var_changed="CaseStatus",
                    prev_state=case1.CaseStatus,
                    current_state=newstate.CaseStatus,
                    action_type=ActionTypes.CASE_CLOSED,
                )
                if case1.Complainer:
                    body = caseClosingMessage(case1)
                    auditlog = AuditLog.objects.create(
                    case=case1,
                    status=case1.CaseStatus,
                    created_by=userRole,
                    prev_state="",
                    current_state="",
                    message=body,
                    action_type=ActionTypes.CASE_CLOSING_MESSAGE_SENT,
                )

            return Response("Success, Case: " + str(case1.CaseNumber) + " is closed")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def sanitiseCaseNature(request):
    cases=Case.objects.all()
    for case in cases:
        if case.CaseNature == "Complain":
            case.CaseNature = CaseNature.COMPLAIN
            case.save()
    return Response("Old Cases were Updated")
