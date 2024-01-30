import json
from rest_framework.request import Request
from accounts.Utils.userRoleParser import parser
from rest_framework.decorators import api_view
from accounts.constants import CaseStatus, UserRole
from accounts.errors import serialer_error
from accounts.models import BaseUserModel, Case, Company, Factory, UserRoleFactory
from accounts.permissions import HasGroupPermission
from accounts.serializers import FactorySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import csv
import os
class FactoryAV(APIView):
    permission_classes = [
        HasGroupPermission
        
    ]
    required_groups = {
        'GET': ['SUPER_ADMIN', 'FACTORY_ADMIN', 'REGIONAL_ADMIN', 'CR','CT','CM'],
        'PUT': ['SUPER_ADMIN', 'FACTORY_ADMIN','REGIONAL_ADMIN'],
        'POST': ['SUPER_ADMIN','REGIONAL_ADMIN'],
        'DELETE': ['SUPER_ADMIN','FACTORY_ADMIN','REGIONAL_ADMIN']
    }
    model = "factory"
    # apiview for list of factories in a company
    @swagger_auto_schema(responses={
        200: openapi.Response('Successful response', FactorySerializer),
        400: 'Invalid request',
    })
    def get(self, request: Request) -> Response:
        if request.GET.get("Company") is None:
            return Response({
                        "errorMessage": "Company missing from params"
                        }
                        ,status= status.HTTP_400_BAD_REQUEST
                        )
        try:
            company=Company.objects.get(pk=request.GET.get("Company"))
        except Company.DoesNotExist:
            return Response(
                    {
                        "errorMessage": "Company with ID {} doesn't exist".format(
                            request.GET.get("Company")
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        userRole=parser(request)
        # if userRole.role.role == UserRole.REGIONAL_ADMIN:
        #     facs = Factory.objects.filter(Company=company,region=userRole.region_fk,is_active=True).order_by('-last_modified')
        # else:
        #     facs = Factory.objects.filter(Company=request.GET.get("Company"),is_active=True).order_by('-last_modified')
        if request.query_params.get("operation")=="region":
            print("yellow")
            facs = Factory.objects.filter(Company=company,region=userRole.region_fk,is_active=True).order_by('-last_modified')
        else:
            print("bajgjawhjka")
            facs = Factory.objects.filter(Company=request.GET.get("Company"),is_active=True).order_by('-last_modified')
        data = []
        cnt = 0
        for fac in facs.iterator():
            serializer = FactorySerializer(fac)
            dt = serializer.data
            dt['Company']=fac.Company.Legalcompanyname
            dt['Company_id']=fac.Company.id
            # factory_admin=BaseUserModel.objects.get(role=UserRole.FACTORY_ADMIN,)
            try:
                factory_admin = UserRoleFactory.objects.get(factory_fk=fac.id,role__role=UserRole.FACTORY_ADMIN,is_active=True)
                dt["FactoryAdmin"]=factory_admin.user_fk.email
            except UserRoleFactory.DoesNotExist:
                dt["FactoryAdmin"]="Factory Admin is not assigned yet"
            except UserRoleFactory.MultipleObjectsReturned:
                dt["FactoryAdmin"]="Multiple Factory Admin exists for this factory please remove the either one"

            data.append(dt)
            cnt = +1
        # print(number,data)
        message = {
                    "message": "Factories for the company {} has been fetched successfully".format(
                        fac.Company.    Legalcompanyname
                    ),
                    "message_body": {"Factories":data}
                }
        return Response(message, status=status.HTTP_200_OK)
    @transaction.atomic
    def post(self, request: Request) -> Response:
        existing_fac_same_number=Factory.objects.filter(Number=request.data['Number'])
        if existing_fac_same_number.count() > 0:
            return Response({
                        'errorMessage': "Invalid Inache Number provided, another Factory uses the same number as this one",
                        'errorStatus': "INVALID_INACHE_NO" 
                        },status=status.HTTP_406_NOT_ACCEPTABLE)    
        try:
            existing_fac=Factory.objects.get(Code=request.data['Code'])
            if existing_fac.is_active==False:
                existing_fac.delete()
        except Factory.DoesNotExist:
            pass
        serializer=FactorySerializer(data=request.data)
        if serializer.is_valid():
            factory=serializer.save()
            message = {
                    "message": "Factory {} for the company {} has been registered successfully".format(
                        factory.Code,factory.Company.Legalcompanyname
                    ),
                    "id":factory.id
                }
            return Response(message, status=status.HTTP_200_OK)
            # return(Response("Factory Registered"))
        else:
            error_response=serialer_error(serializer.errors)
            return Response(
                            error_response
            ,status=status.HTTP_400_BAD_REQUEST)
    def put(self, request: Request) -> Response:
        if request.GET.get("id") is None:
            return Response(
                {
                        "errorMessage": "Factory missing from params"
                        }
                        ,status= status.HTTP_400_BAD_REQUEST
            )
        try:
            # if (self.request.user.id==request.GET.get("user")) write the logic of giving thr permission to crcmct to change theor profile pic in permissions.py
            # print(BUMDetails)
            fac = Factory.objects.get(pk=request.GET.get("id"),is_active=True)

        except Factory.DoesNotExist:
            return Response(
                {
                        "errorMessage": "Factory with ID {} doesn't exist".format(
                            request.GET.get("id")
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
            )
        userRole=parser(request)
        if userRole.role.role ==UserRole.FACTORY_ADMIN and userRole.factory_fk.id!=fac.id:
            return Response(
                {
                        "errorMessage": "You are not allowed to edit this factory"
                    },
                    status=status.HTTP_403_FORBIDDEN,
            )
        # if condition for when usertole if factory admin and if factory admin is tryig to chage attributes other than requiredAwarenessProgram
        if userRole.role.role ==UserRole.FACTORY_ADMIN and request.data.get("requiredAwarenessProgram")==fac.requiredAwarenessProgram :
            return Response(
                {
                        "errorMessage": "You are not allowed to edit factory details other than requiredAwarenessProgram"
                    },
                    status=status.HTTP_403_FORBIDDEN,
            )
        elif userRole.role.role ==UserRole.FACTORY_ADMIN and request.data.get("requiredAwarenessProgram")!=fac.requiredAwarenessProgram:
            serializer = FactorySerializer(fac, data=request.data)
            if serializer.is_valid():
                serializer.save()
                message = {
                        "message": "Factory {} for the company {} has been edited successfully".format(
                            fac.Code,fac.Company.Legalcompanyname
                        )
                    }
                return Response(message, status= status.HTTP_200_OK)
            else:
                error_response=serialer_error(serializer.errors)
                return Response(
                                error_response
                ,status=status.HTTP_400_BAD_REQUEST)
            
            
        if(fac.Code!=request.data['Code']):
            try:
                existing_fac=Factory.objects.get(Code=request.data['Code'])
                if existing_fac.is_active==False:
                    existing_fac.delete()
                elif existing_fac.is_active==True and existing_fac.id!=fac.id:
                    return Response(
                    {
                            "errorMessage": "Cannot change the code of the factory because the code is already assigned to a active factory"
                            }
                            ,status= status.HTTP_400_BAD_REQUEST
                )
            except Factory.DoesNotExist:
                pass
       
        if(request.data["Company"]!=fac.Company.id):
            return Response({
                        "errorMessage": "Cannot change Company"
                        }
                        ,status= status.HTTP_400_BAD_REQUEST)
        serializer = FactorySerializer(fac, data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = {
                    "message": "Factory {} for the company {} has been edited successfully".format(
                        fac.Code,fac.Company.Legalcompanyname
                    )
                }
            return Response(message, status= status.HTTP_200_OK)
        else:
            error_response=serialer_error(serializer.errors)
            return Response(
                            error_response
            ,status=status.HTTP_400_BAD_REQUEST)
    @transaction.atomic
    def delete(self, request: Request) -> Response:
        response={}
        try:
            fac = Factory.objects.get(pk=request.GET.get("id"),is_active=True)
        except Factory.DoesNotExist:
            return Response(
                {
                        "errorMessage": "Factory with ID {} doesn't exist".format(
                            request.GET.get("id")
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
            )
        cases=Case.objects.filter(Factory=fac.id,Company=fac.Company,CaseStatus__in=[
                    CaseStatus.ASSIGNED_TO_TROUBLESHOOTER, CaseStatus.UNDER_INVESTIGATION,CaseStatus.ASSIGNED_TO_REPORTER,CaseStatus.ASSIGNED_TO_MANAGER,CaseStatus.RESOLVED])
        if cases.count()==0:
            fac.is_active=False
            users=UserRoleFactory.objects.filter(factory_fk=fac.id,role__role__in=[UserRole.CASE_REPORTER,UserRole.CASE_MANAGER,UserRole.CASE_TROUBLESHOOTER])
            for user in users:
                user.is_active=False
                user.save()
            try:
                admin_user=UserRoleFactory.objects.get(factory_fk=fac.id,role__role=UserRole.SUPER_ADMIN)
                random_fac=Factory.objects.filter(Company=fac.Company,is_active=True).exclude(id=fac.id)
                if random_fac.count()!=0:
                    random_fac=random_fac.first()
                    admin_user.factory_fk=random_fac
                    admin_user.save()
                else:
                    message={
                        "errorMessage": "Can’t Delete Factory {}: Only one Factory remaining for this company".format(
                            fac.Code
                        )}
                    return Response(message,status.HTTP_400_BAD_REQUEST)
            except UserRoleFactory.DoesNotExist:
                pass
            #disable factory users too
        else:
            message={
                        "errorMessage": "Can’t Delete Factory {} with Pending cases : The selected Factory has pending cases left. Please clear those before deleting the Factory data.".format(
                            fac.Code
                        )
            }
           
            return Response(message,status=status.HTTP_403_FORBIDDEN)
        
        fac.save()
        message = {
                    "message": "Factory {} for the Company {} has been deleted successfully".format(
                        fac.Code,fac.Company.Legalcompanyname
                    )
                }
                
        return Response(message,status.HTTP_200_OK)



fss = FileSystemStorage(location="codes/")

@api_view(['POST', 'PUT'])
def factoryCodesUpdate(request:Request)->Response:
    file = request.FILES.get('file')
    if not file:
        return Response("No file uploaded", status=status.HTTP_400_BAD_REQUEST)
    file_extension = os.path.splitext(file.name)[1]
    if file_extension.lower() != '.csv':
        return Response("Only CSV files are allowed", status=status.HTTP_400_BAD_REQUEST)
    content = file.read()
    file_content = ContentFile(content)
    file_name = fss.save(
        "codes.csv", file_content
    )
    tmp_file = fss.path(file_name)
    csv_file = open(tmp_file, errors="ignore")
    reader = csv.reader(csv_file)
    next(reader)

    codes = []
    for id_, row in enumerate(reader):
        (OLD_FACTORY, NEW_FACTORY) = row
        try:
            factory=Factory.objects.get(Code=OLD_FACTORY)
            factory.Code=NEW_FACTORY
            factory.save()
        except Factory.DoesNotExist:
            continue

    return Response("Successfully updated factory codes", status=status.HTTP_200_OK)