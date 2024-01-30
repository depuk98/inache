from rest_framework.decorators import api_view
from accounts.models import (
    Company,
    Factory,
    Case,
    Complainer,
    FactoryDepartment
)
from rest_framework.response import Response
import requests
from accounts.constants import CaseStatus
from django.core.cache import cache
from rest_framework import status



def workerDataUpload():
    
    company=Company.objects.get(Legalcompanyname="Shahi Exports PVT LTD")
    factory = Factory.objects.filter(Company=company)

    for fac in factory.iterator():
        code = fac.Code
        url = f'https://careers.shahi.co.in/gblbuddy/api/emp/getempbyfactandmono?fact={code}'
        response = requests.get(url)
        data = response.json()
        existing_complainers = Complainer.objects.filter(Company=company,Factory=fac)
        existing_emails = set(existing_complainers.values_list('PhoneNo', flat=True))
        new_complainers=[]
        new_departments = []
        new_coms={}
        languages = []

        for item in data:
            new_complainers.append(item["mobile"])
            new_departments.append([fac,item["departmentdesc"],item["sectiondesc"]])
            language = item["languagedesc"].split(',')[0]
            languages.append(item["languagedesc"].split(',')[0])

            if item["mobile"] in existing_emails:
                try:
                    complainer = Complainer.objects.get(Factory=fac,Company=company,PhoneNo=item["mobile"])
                except Complainer.MultipleObjectsReturned:
                    complainer = Complainer.objects.filter(PhoneNo=item["mobile"],Factory=fac,Company=company).first()
                    Complainer.objects.filter(PhoneNo=item["mobile"]).exclude(id=complainer.id).delete()

                complainer.Department=item["departmentdesc"]
                complainer.SubDepartment=item["sectiondesc"]
                complainer.Gender=item["genderdesc"]
                complainer.PhoneNo=item["mobile"]
                complainer.Language=language
                complainer.Registered=True
                complainer.save()

            else:
                new_coms[item["mobile"]]=Complainer(
                    Company=company,
                    Factory=fac,
                    Department=item["departmentdesc"],
                    SubDepartment=item["sectiondesc"],
                    Gender=item["genderdesc"],
                    PhoneNo=item["mobile"],
                    Language=language,
                    Registered=True
                )

    delete_complainers=[]
    for comp in existing_complainers:
        if str(comp.PhoneNo) not in new_complainers:
            if Case.objects.filter(Complainer=comp,CaseStatus__in=[CaseStatus.ASSIGNED_TO_REPORTER,CaseStatus.ASSIGNED_TO_MANAGER,CaseStatus.ASSIGNED_TO_TROUBLESHOOTER,CaseStatus.RESOLVED,CaseStatus.UNDER_INVESTIGATION,CaseStatus.RE_INVESTIGATION]).exists():
                new_departments.append([comp.Factory,comp.Department,comp.SubDepartment])
                continue
            delete_complainers.append(comp)

    unique_lists = [list(t) for t in set(tuple(l) for l in new_departments)]
    unique_languages = set(languages)

    for dept in unique_lists:
        try:
            FactoryDepartment.objects.get(factory=dept[0],Department=dept[1],SubDepartment=dept[2])
        except:
            FactoryDepartment.objects.create(factory=dept[0],Department=dept[1],SubDepartment=dept[2])

    Complainer.objects.bulk_create(list(new_coms.values()))
    Complainer.objects.filter(pk__in=[complainer.pk for complainer in delete_complainers]).update(is_active=False)
    #print("work done")

    cache_key = "languagesUpdate"
    cache.set(cache_key, unique_languages, None)

    print("languages are: ",cache.get(cache_key))

    return "data uploaded"



@api_view(["GET"])
def getLanguages(request):
        try:
            cache_key = "languagesUpdate"
            languages = cache.get(cache_key)
            if languages == None:
                return Response(
                    {
                        "languages": ["English","Hindi"]
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "languages": languages
                    },
                    status=status.HTTP_200_OK,
                )

        except:
            return Response(
                {
                    "errorMessage": "No Cache Data found"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

@api_view(["GET"])
def masterDataUpload(request):
    return Response(workerDataUpload())
