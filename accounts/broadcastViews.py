from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from accounts.Utils.userRoleParser import parser
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from drf_yasg import openapi
from django.db.models import Q, F
from collections import defaultdict
import os
import re
import json
import requests
from django.apps import apps
from accounts.constants import UserRole, Status
from accounts.utils import current_time
from accounts.models import (
    FactoryDepartment,
    Company,
    Factory,
    SMSTemplates,
    Case,
    Complainer,
    BroadcastMessage
)
from accounts.serializers import (
    FactoryDepartmentSerializer,
    CompanySerializer,
    SMSTemplatesSerializer,
    BroadcastMessageSerializer,
    ComplainerSerializer
)

class TemplateDetails(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('companyID', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ID of the company'),
            openapi.Parameter('temp_category', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='category of the template'),
            openapi.Parameter('templateID', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ID of the template'),
        ]
    )
    def get(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        if request.query_params.get("companyID") and request.query_params.get(
            "temp_category"
        ):
            try:
                company = Company.objects.get(id=request.query_params.get("companyID"))
                # temp_cat = []
                user_role = []
                # temp_cat.append(request.query_params.get("temp_category"))
                temp_cat = request.query_params.get('temp_category').split(',')
                user_role.append(userRole.role.role)
                q_objects = Q()
                for category in temp_cat:
                    q_objects |= Q(template_categories__contains=[category])
                data = (
                    SMSTemplates.objects.filter(
                    Company=request.query_params.get("companyID"),
                    # template_categories__contains=temp_cat,
                    user_roles_access__contains=user_role
                    ).filter(q_objects).values('Title', 'language')
                    .annotate(templateID=F('templateID'))
                )
                result = defaultdict(dict)
                for item in data:
                    result[item['Title']][item['language']] = item['templateID']
                result = dict(result)
                # factory =userRole.factory_fk.id
                # departments = FactoryDepartment.objects.filter(factory=factory)
                # DepartmentSerializer = FactoryDepartmentSerializer(departments,many=True)
                company_serializer = CompanySerializer(company)
                message = {
                    "message": "Templates for the company {} has been fetched successfully".format(
                        company_serializer.data["Legalcompanyname"]
                    ),
                    "message_body": {"templates":result}#,"departments":DepartmentSerializer.data}
                }
                return Response(message, status=status.HTTP_200_OK)
            except Company.DoesNotExist:
                return Response(
                    {
                        "errorMessage": "Company with Id {} doesn't exist".format(
                            request.query_params.get("companyID")
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                    {
                        "errorMessage": "Please Give Relevant Query Parameters to get the Data"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
    def post(self, request: Request) -> Response:
        if request.query_params.get("templateID") or request.query_params.get("department") or request.query_params.get("caseID") or request.query_params.get("gender") or request.query_params.get("language") or request.query_params.get("draftID"):
            try:
                # factory =userRole.factory_fk.id
                userRole=parser(request)
                if userRole is None:
                    return Response({"error":"ROLE ID NOT PRESENT"})
                user_id = userRole.id
                company = userRole.user_fk.company_fk.id
                cache_key = f'user_data_{user_id}_first'
                data = cache.get(cache_key)
                if data == None:
                    data = {}
                # data["factory"] = factory
                data["company"] = company
                comb = []
                if request.query_params.get("templateID"):
                    templates = request.query_params.get("templateID")
                    temps = templates.split(',')
                if request.query_params.get("gender"):
                    gen = request.query_params.get('gender')
                    gender = gen.split(',')
                    data["gender"] = gender
                if request.query_params.get("language"):
                    lan = request.query_params.get('language')
                    language = lan.split(',')
                    data["language"] = language
                if request.query_params.get('department'):
                    departments = json.loads(request.data['departments'])
                    # departments = json.loads(request.query_params.get('department'))
                    # deps = department.split(',')
                    # depts = FactoryDepartment.objects.filter(id__in=deps)
                    # departments = {}
                    # for dep in depts:
                    #     if dep.Department not in departments:
                    #         departments[dep.Department] = []
                    #     departments[dep.Department].append(dep.SubDepartment)
                    data["departments"] = departments

                # autofilling for broadcast messages
                if request.query_params.get('templateID') and request.query_params.get('department'):
                    for tem in temps:
                        template = SMSTemplates.objects.get(templateID=int(tem),Company=company)
                        serializer = SMSTemplatesSerializer(template)
                        for dept in departments:
                            for sub in departments[dept]:
                                for factory_id in data["factories"]: 
                                    matches = re.findall(r"\&@{(.+?)}",serializer.data["body"])
                                    body=serializer.data["body"]
                                    for match in matches:
                                        words = match.split(".")
                                        try:
                                            model = apps.get_model(app_label="accounts", model_name=words[0])
                                            if words[0] == "Case":
                                                value = model.objects.get(id=request.query_params.get("caseID")).__getattribute__(words[1])
                                            elif words[0] == "Factory":
                                                value = model.objects.get(id=factory_id).__getattribute__(words[1])
                                            elif words[1] == "Department":
                                                value = dept
                                            elif words[1] == "SubDepartment":
                                                value = sub
                                            else:
                                                continue
                                            body = re.sub(fr"\&@{{{match}\}}", str(value), body)
                                        except:
                                            continue
                                    temp = {"templateID":serializer.data['templateID'],"Title":serializer.data['Title'],"body":body,"language":serializer.data['language'],"variables":serializer.data['variables'],"Department":dept,"SubDepartment":sub,"Company":serializer.data['Company'],"Factory":factory_id}
                                    comb.append(temp)

                # autofilling for ct send message templates
                elif request.query_params.get('templateID') and request.query_params.get('caseID'):
                    #factory =userRole.factory_fk.id
                    factory = Case.objects.get(id=request.query_params.get("caseID")).Factory.id
                    data["factories"] = [factory]
                    for tem in temps:
                        template = SMSTemplates.objects.get(templateID=int(tem),Company=company)
                        serializer = SMSTemplatesSerializer(template)
                        matches = re.findall(r"\&@{(.+?)}",serializer.data["body"])
                        body=serializer.data["body"]
                        data["caseID"] = request.query_params.get('caseID')
                        #if request.query_params.get("caseID"):
                        if Case.objects.get(id=request.query_params.get("caseID")).Complainer:
                            number = Case.objects.get(id=request.query_params.get("caseID")).Complainer
                        for match in matches:
                            words = match.split(".")
                            try:
                                model = apps.get_model(app_label="accounts", model_name=words[0])
                                if words[0] == "Case":
                                    value = model.objects.get(id=request.query_params.get("caseID")).__getattribute__(words[1])
                                elif words[0] == "Factory":
                                    value = model.objects.get(id=factory).__getattribute__(words[1])
                                elif words[1] == "Department":
                                    if Complainer.objects.get(PhoneNo=number).__getattribute__("Department"):
                                        value = Complainer.objects.get(PhoneNo=number).__getattribute__("Department")
                                    else:
                                        value = "Department"
                                elif words[1] == "SubDepartment":
                                    value = Complainer.objects.get(PhoneNo=number).__getattribute__("SubDepartment")
                                    if Complainer.objects.get(PhoneNo=number).__getattribute__("SubDepartment"):
                                        value = Complainer.objects.get(PhoneNo=number).__getattribute__("SubDepartment")
                                    else:
                                        value = "SubDepartment"
                                else:
                                    continue
                                body = re.sub(fr"\&@{{{match}\}}", str(value), body)
                            except:
                                continue
                        temp = {"templateID":serializer.data['templateID'],"Title":serializer.data['Title'],"body":body,"language":serializer.data['language'],"variables":serializer.data['variables'],"Company":serializer.data['Company']}
                        comb.append(temp)
                else:
                    return Response(
                    {
                        "errorMessage": "Please Give Relevant Query Parameters to get the Data"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
                data["templates"] = comb
                list = []
                variables = json.loads(comb[0]["variables"])
                noOfInputs = len(variables)
                data['variables']= variables
                data['noOfInputs']=noOfInputs
                data['done']="No"
                cache.set(cache_key, data, 3600)
                # need to provide user input values for autofil if editing a draft
                if request.query_params.get('draftID'):
                    inputs = BroadcastMessage.objects.get(id=request.query_params.get('draftID')).inputVariables
                    for key,value in variables.items():
                        list.append({"var":{key:value},"InputValue":inputs[value],"language":language})   
                else:
                    for key,value in variables.items():
                        list.append({"var":{key:value},"language":language})
                message = {
                    "message": "Variables for templateId {} has been fetched successfully".format(
                        request.query_params.get("templateID")
                    ),
                    "message_body": list,
                }
                return Response(message, status=status.HTTP_200_OK)
            except SMSTemplates.DoesNotExist:
                return Response(
                    {
                        "errorMessage": "Template with ID {} doesn't exist".format(
                            request.query_params.get("templateID")
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                    {
                        "errorMessage": "Please Give Relevant Query Parameters to get the Data"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

    # @swagger_auto_schema(request_body=SMSTemplatesSerializer)
    # def post(self, request: Request) -> Response:
    #     data = request.data
    #     try:
    #         temp = SMSTemplates.objects.get(templateID=data["templateID"])
    #         serializer = SMSTemplatesSerializer(temp)
    #         message = {
    #             "errorMessage": "A template with templateId {} already exists".format(
    #                 data["templateID"]
    #             ),
    #             "message_body": serializer.data,
    #         }
    #         return Response(message, status=status.HTTP_200_OK)
    #     except SMSTemplates.DoesNotExist:
    #         matches = re.findall(r"\${(.+?)}", data["body"])
    #         data["variables"] = {str(i): value for i, value in enumerate(matches)}
    #         serializer = SMSTemplatesSerializer(data=data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             message = {
    #                 "message": "A template with templateId {} is created successfully".format(
    #                     serializer.data["templateID"]
    #                 ),
    #                 "message_body": serializer.data,
    #             }
    #             return Response(message, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='patch',
        request_body=SMSTemplatesSerializer,
        manual_parameters=[
            openapi.Parameter(
                'templateID',
                openapi.IN_QUERY,
                description='The ID of the template to update',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    @action(detail=True, methods=['patch'])
    def patch(self, request: Request) -> Response:
        try:
            template = SMSTemplates.objects.get(
                templateID=request.query_params.get("templateID")
            )
            serializer = SMSTemplatesSerializer(
                template, data=request.data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = {
                    "message": "Template with templateId {} has been updated successfully".format(
                        serializer.data["templateID"]
                    ),
                    "message_body": serializer.data,
                }
                return Response(message, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SMSTemplates.DoesNotExist:
            return Response(
                {
                    "errorMessage": "Template with ID {} doesn't exist".format(
                        request.query_params.get("templateID")
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('templateID', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='ID of the template'),
        ]
    )

    def delete(self, request: Request) -> Response:
        try:
            template = SMSTemplates.objects.get(
                templateID=request.query_params.get("templateID"), Company=request.query_params.get("companyID")
            )
            template.delete()
            message = {
                "message": "Template with templateId {} has been Deleted successfully".format(
                    request.query_params.get("templateID")
                )
            }
            return Response(message, status=status.HTTP_204_NO_CONTENT)
        except SMSTemplates.DoesNotExist:
            return Response(
                {
                    "errorMessage": "Template with ID {} doesn't exist".format(
                        request.query_params.get("templateID")
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

@api_view(["GET"])
def departmentlist(request):
    data={}
    payload=request.query_params.get("factories")
    factories=payload.split(",")
    data["factories"]=factories
    total_departments=[]
    for factory in factories:
        departments = FactoryDepartment.objects.filter(factory=factory).values("Department","SubDepartment")
        total_departments.extend(departments)
    unique_departments = []
    seen = set()
    for dept in total_departments:
        identifier = (dept['Department'], dept['SubDepartment'])
        if identifier not in seen:
            seen.add(identifier)
            unique_departments.append(dept)
    userRole=parser(request)
    if userRole is None:
        return Response({"error":"ROLE ID NOT PRESENT"})
    user_id = userRole.id
    cache_key = f'user_data_{user_id}_first'
    cache.set(cache_key, data, 3600)
    message = {
        "message": "Unique Departments for the given factories has been fetched successfully",
        "message_body": {"departments":unique_departments}
    }
    return Response(message, status=status.HTTP_200_OK)


def translate_text(text, source_language, target_language):
    url = 'https://translation.googleapis.com/language/translate/v2'
    params = {
        'q': text,
        'source': source_language,
        'target': target_language,
        'format': 'text',
        'key': "AIzaSyACkHh4OiTy5LH2LWaZwldy23hKz7NJtc4"
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json()['data']['translations'][0]['translatedText']
    else:
        return None

class VariableMapping(APIView):
    def get(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        user_id = userRole.id
        cache_key = f'user_data_{user_id}_first'
        data = cache.get(cache_key)
        if data == None:
            return Response(
                {
                    "errorMessage": "Please Select Template and Language"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if request.query_params.get('inputs'):
            inputs_str = request.query_params.get('inputs')
            inputs = json.loads(inputs_str) if inputs_str else {}
            if data['noOfInputs']!=len(inputs):
                return Response(
                {
                    "errorMessage": "Please give Input for all the Variables"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
            dict = {}
            data['inputs'] = inputs
            languages = data['language']
            templates = data['templates']
            comb=[]
            matchBody = templates[0]["body"]
            matches = re.findall(r"\${(.+?)}", matchBody)
            key = {"Hindi":'hi',"Kannada":'kn',"Punjabi":'pa',"Telugu":'te',"Tamil":'ta',"Oriya":'or'}
            # for each language, need to filter that language templates
            for lang in languages:
                dict[lang]={}
                # translating all the matches to this language
                for match in matches:
                    try:
                        if lang == "English":
                            value = inputs[match]
                        else:
                            value = translate_text(inputs[match],'en',key[lang])
                        dict[lang][match] = value
                    except:
                        continue
                # for each language, need to filter that language templates
                filled_message = list(filter(lambda x: x.get("language") == lang, templates))
                for template in filled_message:
                    body = template["body"]
                    # for each match, replace the word with translated value in body
                    for match in matches:
                        value=dict[lang][match]
                        body = re.sub(fr"\${{{match}\}}", str(value), body)
                    temp = {"templateID":template['templateID'],"Title":template['Title'],"body":body,"language":template['language'],"variables":template['variables'],"Company":template['Company']}
                    comb.append(temp)
            data['templates'] = comb
            data['done'] = "Yes"
            cache.set(cache_key, data, 3600)
            message = {
                "message": "Variables for the templateId {} has been mapped successfully".format(
                            templates[0]["templateID"]
                        ),
                        "message_body": comb,
                    }
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response(
                    {
                        "errorMessage": "Pass the Input Variables"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

class FilterTemplates(APIView):  
    def get(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        user_id = userRole.id
        cache_key = f'user_data_{user_id}_first'
        data = cache.get(cache_key)
        if data == None:
            return Response(
                {
                    "errorMessage": "Please complete filters screen"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if request.query_params.get('inputs'):
            inputs_str = request.query_params.get('inputs')
            inputs = json.loads(inputs_str) if inputs_str else {}
            if data['noOfInputs']!=len(inputs):
                return Response(
                {
                    "errorMessage": "Please give Input for all the Variables"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
            dict = {}
            data['inputs'] = inputs
            languages = data['language']
            templates = data['templates']
            comb=[]
            matchBody = templates[0]["body"]
            matches = re.findall(r"\${(.+?)}", matchBody)
            key = {"Hindi":'hi',"Kannada":'kn',"Punjabi":'pa',"Telugu":'te',"Tamil":'ta',"Oriya":'or'}
            for lang in languages:
                dict[lang]={}
                # translating all the matches to this language
                for match in matches:
                    try:
                        if lang == "English":
                            value = inputs[match]
                        else:
                            value = translate_text(inputs[match],'en',key[lang])
                        dict[lang][match] = value
                    except:
                        continue
                # for each language, need to filter that language templates
                filled_message = list(filter(lambda x: x.get("language") == lang, templates))
                for template in filled_message:
                    body = template["body"]
                    # for each match, replace the word with translated value in body
                    for match in matches:
                        value=dict[lang][match]
                        body = re.sub(fr"\${{{match}\}}", str(value), body)
                    temp = {"templateID":template['templateID'],"Title":template['Title'],"body":body,"language":template['language'],"variables":template['variables'],"Department":template['Department'],"SubDepartment":template['SubDepartment'],"Company":template['Company'],"Factory":template['Factory']}
                    comb.append(temp)
            data['templates'] = comb
            cache.set(cache_key, data, 3600)
        else:
            pass
        snt_msgs = Complainer.objects.filter(Factory__in=data['factories'],is_active=True) #1 -> all complainers in selected factories
        departments = data['departments']
        format_departments=[]
        for item in departments:
            for subd in departments[item]:
                format_departments.append({"Department":item,"SubDepartment":subd})
        language = data['language']
        gender = data['gender']
        factories = data['factories']
        factory_values = Factory.objects.filter(id__in=factories).values('id','Code')
        deptid= []
        q_gender = Q(Gender__in=gender)
        # q_language = Q(Language__in=language)
        q_dept=Q()
        for dep in departments:
            for sub in departments[dep]:
                # deptid.append(FactoryDepartment.objects.get(SubDepartment=sub,Department=dep,factory=factory).id)
                q_dept |= (Q(Department=dep) & Q(SubDepartment=sub))
        q = q_gender & q_dept
        # depart = FactoryDepartment.objects.filter(id__in=deptid)
        # DepartmentSerializer = FactoryDepartmentSerializer(depart,many=True)
        complainers = snt_msgs.filter(q)
        #final set of complainers that need to receive msgs
        filter_complainers = 0
        filter_message = None
        message_body = data['templates']
        data['sendCount'] = complainers.count()
        data['deptid'] = departments
        # filter department and language specific message for preview
        if request.query_params.get("department") and request.query_params.get("language") and request.query_params.get("factory"):
            Lang = request.query_params.get("language")
            depment = json.loads(request.query_params.get('department'))
            factory = request.query_params.get("factory")
            deptment, subdeptment = next(iter(depment.items()))
            # deptment = FactoryDepartment.objects.get(id=depment).Department
            # subdeptment = FactoryDepartment.objects.get(id=depment).SubDepartment
            language.remove("English")
            if Lang != "English":
                filter_complainers = complainers.filter(Language=Lang,Department=deptment,SubDepartment=subdeptment,Factory=factory).count()
                filter_message = list(filter(lambda x: x.get("Department") == deptment and x.get("SubDepartment") == subdeptment and x.get("language") == Lang and x.get("Factory") == factory, message_body))
            elif Lang == "English":
                filter_complainers = complainers.filter(Department=deptment,SubDepartment=subdeptment,Factory=factory).exclude(Language__in=language).count()
                filter_message = list(filter(lambda x: x.get("Department") == deptment and x.get("SubDepartment") == subdeptment and x.get("language") == "English" and x.get("Factory") == factory, message_body))
            language = ["English"] + language
            data['language'] = language
            cache.set(cache_key, data, 3600)
            message = {
                        "message": "Preview Data with Filters of SubDepartment {} and Language {} has been fetched Successfully".format(
                            subdeptment,request.query_params.get("language")
                        ),
                        "message_body": {"TotalSMSCount":complainers.count(),"Gender":gender,"subDepartments": format_departments, "language":language, "Factories":factory_values,"FilteredCount": filter_complainers, "FilteredPreview":filter_message[0]["body"]},
                    }
            return Response(message, status=status.HTTP_200_OK)
        elif request.query_params.get('inputs'):
            cache.set(cache_key, data, 3600)
            message = {
                        "message": "Preview Data has been fetched Successfully".format(
                            request.query_params.get("department"),request.query_params.get("language")
                        ),
                        "message_body": {"TotalSMSCount":complainers.count(),"Gender":gender,"subDepartments": format_departments, "language":language, "Factories":factory_values},
                    }
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "errorMessage": "Please Select all the relevant fields in the Filters Screen"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

class BroadcastDraft(APIView):
    def get(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        q_userdynamic = Q()
        q_complainerdynamic = Q()
        if userRole.role.role == UserRole.SUPER_ADMIN:
            q_userdynamic &= Q(Company=userRole.user_fk.company_fk)
            q_complainerdynamic &= Q(Factory__Company=userRole.user_fk.company_fk)
        elif userRole.role.role == UserRole.REGIONAL_ADMIN:
            q_userdynamic &= Q(createdBy=userRole.user_fk.user_name + " (" + userRole.role.role + ")")
            q_complainerdynamic &= Q(Factory__region=userRole.region_fk)
        if request.query_params.get("category"):
            try:
                if request.query_params.get("category") == Status.DRAFT:
                    data = BroadcastMessage.objects.filter(
                        q_userdynamic,
                        status__in = [Status.DRAFT,Status.MODIFIED]
                    )
                elif request.query_params.get("category") == Status.SENT:  
                    data = BroadcastMessage.objects.filter(
                        q_userdynamic,
                        status = Status.SENT
                    )      
                comb=[]
                for templates in data:
                    serializer = BroadcastMessageSerializer(templates)
                    message_body = list(filter(lambda x: x.get("language") == "English", serializer.data["messageBody"]))
                    Langauges = ', '.join(serializer.data["Languages"])
                    if serializer.data["createdBy"] == str(request.user.user_name + " (" + userRole.role.role + ")"):
                        comb.append({"editAccess":"Yes","id":serializer.data["id"],"TotalCount":serializer.data["sendCount"],"lastModified":serializer.data["lastModified"],"createdBy":serializer.data["createdBy"],"languages":Langauges,"templateTitle":serializer.data["templateTitle"],"Message":message_body[0]["body"]})
                    else:
                        comb.append({"editAccess":"No","id":serializer.data["id"],"TotalCount":serializer.data["sendCount"],"lastModified":serializer.data["lastModified"],"createdBy":serializer.data["createdBy"],"languages":Langauges,"templateTitle":serializer.data["templateTitle"],"Message":message_body[0]["body"]})
                sortedDrafts= sorted(comb, key=lambda x: x['lastModified'], reverse=True)
                message = {
                    "message": "Draft Templates has been fetched successfully",
                    "message_body": sortedDrafts
                }
                return Response(message, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {
                        "errorMessage": e,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        elif request.query_params.get("draftID"):
            try:
                draft = BroadcastMessage.objects.get(id=request.query_params.get("draftID"))
                # if the draft is edited and not discarded, when sending broadcast it has no values to fetch from cache, so change back to draft
                if draft.status == Status.MODIFIED:
                    serializer = BroadcastMessageSerializer(draft)
                    draftSerializer = serializer.data
                    draftSerializer["status"] = Status.DRAFT
                    serializer = BroadcastMessageSerializer(draft,data=draftSerializer, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                serializer = BroadcastMessageSerializer(draft)
                if serializer.data["createdBy"] == str(request.user.user_name + " (" + userRole.role.role + ")"):
                    Access = "Yes"
                else:
                    Access = "No"
                factoryComplainers = Complainer.objects.filter(q_complainerdynamic,is_active=True)
                departments = draft.Departments
                language = draft.Languages
                gender = draft.Genders
                factories = draft.factories
                factory_values = Factory.objects.filter(id__in=factories).values('id','Code')
                format_departments=[]
                for item in departments:
                    for subd in departments[item]:
                        format_departments.append({"Department":item,"SubDepartment":subd})
                # depts = FactoryDepartment.objects.filter(id__in=department)
                # DepartmentSerializer = FactoryDepartmentSerializer(depts, many=True)
                # departments = {}
                # for dep in depts:
                #     if dep.Department not in departments:
                #         departments[dep.Department] = []
                #     departments[dep.Department].append(dep.SubDepartment)
                # need to filter below way to avoid complainer mixup with same subdepartment name from different departments
                q_gender = Q(Gender__in=gender)
                q_dept=Q()
                for dep in departments:
                    for sub in departments[dep]:
                        q_dept |= (Q(Department=dep) & Q(SubDepartment=sub))
                q = q_gender & q_dept
                complainers = factoryComplainers.filter(q)
                if draft.status == Status.DRAFT:
                    total_complainers = complainers.count()
                elif draft.status == Status.SENT:
                    total_complainers = draft.sendCount
                filter_complainers = 0
                filter_message = None
                message_body = draft.messageBody
                if request.query_params.get("department") and request.query_params.get("language") and request.query_params.get("factory"):
                    Lang = request.query_params.get("language")
                    depment = json.loads(request.query_params.get('department'))
                    factory = request.query_params.get("factory")
                    deptment, subdeptment = next(iter(depment.items()))
                    # deptment = FactoryDepartment.objects.get(id=depment).Department
                    # subdeptment = FactoryDepartment.objects.get(id=depment).SubDepartment
                    language.remove("English")
                    if Lang != "English":
                        if draft.status == Status.DRAFT:
                            filter_complainers = complainers.filter(Language=Lang,Department=deptment,SubDepartment=subdeptment,Factory=factory).count()
                        elif draft.status == Status.SENT:
                            flter_complainers = list(filter(lambda x: x.get("Department") == deptment and x.get("SubDepartment") == subdeptment and x.get("language") == Lang and x.get("Factory") == factory, message_body))
                            filter_complainers = flter_complainers[0]["SMSCount"]
                        filter_message = list(filter(lambda x: x.get("Department") == deptment and x.get("SubDepartment") == subdeptment and x.get("language") == Lang and x.get("Factory") == factory, message_body))
                    elif Lang == "English":
                        if draft.status == Status.DRAFT:
                            filter_complainers = complainers.filter(Department=deptment,SubDepartment=subdeptment,Factory=factory).exclude(Language__in=language).count()
                        elif draft.status == Status.SENT:
                            flter_complainers = list(filter(lambda x: x.get("Department") == deptment and x.get("SubDepartment") == subdeptment and x.get("language") == "English" and x.get("Factory") == factory, message_body))
                            filter_complainers = flter_complainers[0]["SMSCount"]
                        filter_message = list(filter(lambda x: x.get("Department") == deptment and x.get("SubDepartment") == subdeptment and x.get("language") == "English" and x.get("Factory") == factory, message_body))
                    language = ["English"] + language
                    message = {
                        "message": "Draft with draftID {} has been fetched successfully".format(
                            serializer.data["id"]
                        ),
                        "message_body": {"editAccess":Access,"Status":serializer.data["status"],"draftID":serializer.data["id"],"templateIDs":serializer.data["templateIDs"],"TotalSMSCount":total_complainers,"subDepartments": format_departments, "language":language, "Factories":factory_values, "lastModified":serializer.data["lastModified"],"createdBy":serializer.data["createdBy"],"Template":serializer.data["templateTitle"], "SMSCount": filter_complainers, "Message":filter_message[0]["body"],"Genders":draft.Genders},
                    }
                    return Response(message, status=status.HTTP_200_OK)
                else:
                    message = {
                        "message": "Draft with draftID {} has been fetched successfully".format(
                            serializer.data["id"]
                        ),
                        "message_body": {"editAccess":Access,"Status":serializer.data["status"],"draftID":serializer.data["id"],"templateIDs":serializer.data["templateIDs"],"TotalSMSCount":total_complainers,"subDepartments": format_departments, "language":language, "Factories":factory_values, "lastModified":serializer.data["lastModified"],"createdBy":serializer.data["createdBy"],"Template":serializer.data["templateTitle"],"Genders":draft.Genders},
                    }
                    return Response(message, status=status.HTTP_200_OK)
            except BroadcastMessage.DoesNotExist:
                return Response(
                    {
                        "errorMessage": "Draft with ID {} doesn't exist".format(
                            request.query_params.get("draftID")
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                    {
                        "errorMessage": "Please give a Category or DraftID in Query Params to get Data"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

    # taking values from cache instead of frontend to save a draft
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
            factories = data['factories'],
            Company = Company.objects.get(id=data['company']),
            status = Status.DRAFT,
            Genders = data['gender'],
            templateIDs = list(set(templateIDs)),
            inputVariables = data['inputs'],
            sendCount = data['sendCount'],
            Departments = data['deptid']
        )
        draft.save()
        cache.delete(cache_key)  # Delete data from cache
        serializer = BroadcastMessageSerializer(draft)
        message = {
            "message": "Draft is saved successfully".format(),
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
            draft = BroadcastMessage.objects.get(
                id=request.query_params.get("draftID")
            )
            serializer = BroadcastMessageSerializer(draft)
            draftSerializer = serializer.data
            draftSerializer["lastModified"] = current_time()
            draftSerializer["status"] = Status.DRAFT
            draftSerializer["Languages"] = data['language']
            draftSerializer["messageBody"] = data['templates']
            draftSerializer["Genders"] = data['gender']
            draftSerializer["sendCount"] = data['sendCount']
            draftSerializer["templateIDs"] = list(set(templateIDs))
            draftSerializer["inputVariables"] = data['inputs']
            draftSerializer["Departments"] = data['deptid']
            draftSerializer["factories"] = data['factories']
            serializer = BroadcastMessageSerializer(
                draft, data=draftSerializer, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = {
                    "message": "Draft is saved successfully".format(),
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


class EditDraft(APIView):
    def get(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        if request.query_params.get("draftID"):
            draft = BroadcastMessage.objects.get(id=request.query_params.get("draftID"))
            serializer = BroadcastMessageSerializer(draft)
            draftSerializer = serializer.data
            # if the draft message is edited from draft table
            if request.query_params.get("action") == "edit":
                draftSerializer["status"] = Status.MODIFIED
                serializer = BroadcastMessageSerializer(draft,data=draftSerializer, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                message = {
                    "message": "Draft Status for DraftID {} has been updated to MODIFIED".format(
                        request.query_params.get("draftID")
                    )
                }
                return Response(message, status=status.HTTP_200_OK)
            # if draft message is discarded without midway without sending broadcast
            elif request.query_params.get("action") == "discard":
                user_id = userRole.id
                cache_key = f'user_data_{user_id}_first'
                cache.delete(cache_key)  # Delete data from cache
                draftSerializer["status"] = Status.DRAFT
                serializer = BroadcastMessageSerializer(draft,data=draftSerializer, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                message = {
                    "message": "Draft with DraftID {} has been Discarded successfully".format(
                        request.query_params.get("draftID")
                    )
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                #return Response("Please enter the right draftID and action type")
                return Response(
                    {
                        "errorMessage": "Please enter the right draftID and action type"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

def broadcastmessage(templateID:str, body:str, number:str, company:Company)->int:
    senderid = company.SenderID
    
    to = ",".join(number)
    sid = "HXIN1739327617IN"
    api_key = "Ad434b1d76f34c53b443f89df7b3960a5"
    header = {"api-key": api_key}
    payload = {
        "to": to, 
        "sender": senderid,
        "source": "API",
        "type": "TXN",
        "body": body,
        "template_id": templateID,
    }
    req = requests.post(
        "https://api.kaleyra.io/v1/" + str(sid) + "/messages",
        json=(payload),
        headers=header,
    )
    return req.status_code


class BroadcastMessageAV(APIView):
    def get(self, request: Request) -> Response:
        userRole=parser(request)
        if userRole is None:
            return Response({"error":"ROLE ID NOT PRESENT"})
        try:
            user_id = userRole.id
            cache_key = f'user_data_{user_id}_first'
            data = cache.get(cache_key)
            if request.query_params.get("draftID"):
                draft = BroadcastMessage.objects.get(id=request.query_params.get("draftID"))
                #in draft, if its directly from table, use table data or sending after editing draft, use cache data
                if draft.status == Status.DRAFT:
                    deps = draft.departments
                    depts = FactoryDepartment.objects.filter(id__in=deps)
                    departments = {}
                    for dep in depts:
                        if dep.Department not in departments:
                            departments[dep.Department] = []
                        departments[dep.Department].append(dep.SubDepartment)
                    language = draft.Languages
                    gender = draft.Genders
                    factories = draft.factories
                    message_body = draft.messageBody
                elif draft.status == Status.MODIFIED:
                    departments = data['departments']
                    language = data['language']
                    gender = data['gender']
                    factories = data['factories']
                    message_body = data['templates']
            # if not draft, take all information from cache data
            else:
                departments = data['departments']
                language = data['language']
                gender = data['gender']
                factories = data['factories']
                message_body = data['templates']
            # First, we will send the templates except english ones to the respective complainers
            language.remove("English")
            final = []
            comp=[]
            for dep in departments:
                for sub in departments[dep]:
                    for gen in gender:
                        for factory_id in factories:
                            complainers = Complainer.objects.filter(Factory=factory_id,Department=dep,SubDepartment=sub,Gender=gen,is_active=True)
                            complainerData=ComplainerSerializer(complainers,many=True)
                            production_messages = list(filter(lambda x: x.get("Department") == dep and x.get("SubDepartment") == sub and x.get("Factory") == factory_id, message_body))
                            final.append(production_messages+complainerData.data)
                            comp.append(complainerData.data)
                            for lang in language:
                                if complainers.filter(Language=lang):
                                    final_messages = list(filter(lambda x: x.get("language") == lang, production_messages))
                                    lang_comp = complainers.filter(Language=lang).values('PhoneNo')
                                    #send this complainers in the preferred language
                                    numbers=[]
                                    for com in lang_comp:
                                        numbers.append("+91"+com['PhoneNo'])
                                    sum = len(numbers)
                                    new = list(filter(lambda x: x.get("Department") == dep and x.get("SubDepartment") == sub and x.get("language") == lang and x.get("Factory") == factory_id, message_body))
                                    # storing SMS count of a specific language and department
                                    message_body.remove(new[0])
                                    if new[0].get("SMSCount") != None:
                                        new[0]["SMSCount"] = new[0]["SMSCount"] + sum
                                    else:
                                        new[0]["SMSCount"] = sum
                                    message_body.append(new[0])
                                    Comp = Company.objects.get(id=final_messages[0]['Company'])
                                    # uncomment below line only when you want to send broadcast msgs, accidental running of this function without commenting below line may lead to sending message to so many people
                                    if os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.production':
                                        broadcast_message = broadcastmessage(final_messages[0]['templateID'],final_messages[0]['body'],numbers,Comp)
                                    else:
                                        pass
                                # if there are no complainers for a specific language, the sms count need to be zero
                                else:
                                    final_messages = list(filter(lambda x: x.get("language") == lang, production_messages))
                                    rem=list(filter(lambda x: x.get("Department") == dep and x.get("SubDepartment") == sub and x.get("language") == lang and x.get("Factory") == factory_id, message_body))
                                    message_body.remove(rem[0])
                                    if rem[0].get("SMSCount") != None:
                                        rem[0]["SMSCount"] = rem[0]["SMSCount"]
                                    else:
                                        rem[0]["SMSCount"] = 0
                                    message_body.append(rem[0])
                            # for all the complainer whose prefered language is english and whose preferred language templates are not present will be sent english messages
                            remng_messages = list(filter(lambda x: x.get("language") == "English", production_messages))
                            if complainers.exclude(Language__in = language):
                                remng_comp = complainers.exclude(Language__in = language)
                                #sending this complainers the Default Language i.e, English
                                remnumbers=[]
                                for com in remng_comp.values('PhoneNo'):
                                    remnumbers.append("+91"+com['PhoneNo'])
                                sum = len(remnumbers)
                                new = list(filter(lambda x: x.get("Department") == dep and x.get("SubDepartment") == sub and x.get("language") == "English" and x.get("Factory") == factory_id, message_body))
                                message_body.remove(new[0])
                                if new[0].get("SMSCount") != None:
                                    new[0]["SMSCount"] = new[0]["SMSCount"] + sum
                                else:
                                    new[0]["SMSCount"] = sum
                                message_body.append(new[0])
                                #print(numbers)
                                Comp = Company.objects.get(id=remng_messages[0]['Company'])
                                # uncomment below line only when you want to send broadcast msgs, accidental running of this function without commenting below line may lead to sending message to so many people
                                if os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.production':
                                    broadcast_message = broadcastmessage(remng_messages[0]['templateID'],remng_messages[0]['body'],remnumbers,Comp)
                                else:
                                    pass
                            else:
                                rem=list(filter(lambda x: x.get("Department") == dep and x.get("SubDepartment") == sub and x.get("language") == "English" and x.get("Factory") == factory_id, message_body))
                                message_body.remove(rem[0])
                                if rem[0].get("SMSCount") != None:
                                    rem[0]["SMSCount"] = rem[0]["SMSCount"]
                                else:
                                    rem[0]["SMSCount"] = 0
                                message_body.append(rem[0])
            language = ["English"] + language
            if data:
                data['language'] = language
            # if a draft, need to update the same entry instead of creating new entry
            if request.query_params.get("draftID"):
                draft = BroadcastMessage.objects.get(id=request.query_params.get("draftID"))
                # if directly sending from table, update only relevant fields like time and status
                if draft.status == Status.DRAFT:
                    serializer = BroadcastMessageSerializer(draft)
                    draftSerializer = serializer.data
                    draftSerializer["lastModified"] = current_time()
                    draftSerializer["status"] = Status.SENT
                    draftSerializer["messageBody"] = message_body
                    serializer = BroadcastMessageSerializer(draft,data=draftSerializer, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                # if an edited draft, take values from cache and update the table
                elif draft.status == Status.MODIFIED:
                    serializer = BroadcastMessageSerializer(draft)
                    draftSerializer = serializer.data
                    draftSerializer["lastModified"] = current_time()
                    draftSerializer["status"] = Status.SENT
                    draftSerializer["Languages"] = data['language']
                    draftSerializer["messageBody"] = message_body
                    draftSerializer["Genders"] = data['gender']
                    draftSerializer["sendCount"] = data['sendCount']
                    draftSerializer["Departments"] = data['deptid']
                    draftSerializer["factories"] = data['factories']
                    serializer = BroadcastMessageSerializer(draft,data=draftSerializer, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
            #If a new message, create a fresh entry and take the realtime values from cache
            else:
                #print("cache data when saving is: ",data)
                draft = BroadcastMessage.objects.create(
                createdBy =  request.user.user_name + " (" + userRole.role.role + ")",
                lastModified = current_time(),
                Languages =  data['language'],
                templateTitle = message_body[0]["Title"],
                messageBody =  message_body,
                factories = data['factories'],
                Company = Company.objects.get(id=data['company']),
                status = Status.SENT,
                Genders = data['gender'],
                sendCount = data['sendCount'],
                Departments = data['deptid'],
                )
                draft.save()
            cache.delete(cache_key)  # Delete data from cache
            # print(production_messages)
            message = {
                        "message": "Broadcast Message has been Sent Successfully"
                    }
            return Response(message, status=status.HTTP_200_OK)
        except:
            return Response(
                {
                    "errorMessage": "No Cache Data found"
                },
                status=status.HTTP_404_NOT_FOUND,
            )


#TODO: Need to remove this
@api_view(["GET"])
def sanitizebroadcastmessages(request):
    messages=BroadcastMessage.objects.all()
    for message in messages:
        if message.Genders == ['None']:
            message.Genders = []
        if message.departments==['None']:
            message.departments=[]
        if len(message.factories) == 0 and message.Factory != None:
            message.factories = [message.Factory.id]
            for msg in message.messageBody:
                msg["Factory"] = str(message.Factory.id)
            depts = FactoryDepartment.objects.filter(id__in=message.departments)
            departments = {}
            for dep in depts:
                if dep.Department not in departments:
                    departments[dep.Department] = []
                departments[dep.Department].append(dep.SubDepartment)
            message.Departments = departments
            message.Company = message.Factory.Company
        message.save()
    return Response("Broadcast Messages Updated Successfully", status=status.HTTP_200_OK)



