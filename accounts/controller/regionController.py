from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.Service.regionService import RegionService
from rest_framework.request import Request
from accounts.models import Company, FactoryRegion, Factory
from rest_framework.decorators import api_view
from accounts.Utils.userRoleParser import parser
from rest_framework import status
from accounts.permissions import HasGroupPermission

class RegionDetails(APIView):
    # permission_classes = [
    #      hasregion_permission
        
    # ]
    permission_classes = [
        HasGroupPermission
        
    ]
    required_groups = {
        'GET': ['SUPER_ADMIN', 'REGIONAL_ADMIN', 'CR', 'CM', 'CT'],
        'PUT': ['SUPER_ADMIN'],
        'POST': ['SUPER_ADMIN'],
        'PATCH': ['SUPER_ADMIN'],
        'DELETE': ['SUPER_ADMIN']
    }
    model = "factoryregion"

    def get(self, request:Request)->Response:
        regionService = RegionService(request)
        message,status=regionService.getFactoryRegion()
        if message is None:
            return Response({"error":"ROLE ID NOT PRESENT"},status=status)
        return Response(message,status=status)
    
    def post(self, request:Request)->Response:
        regionService=RegionService(request)
        message,status=regionService.createRegion()
        if message is None:
            return Response({"error":"ROLE ID NOT PRESENT"},status=status)
        return Response(message,status=status)

    def patch(self, request:Request)->Response:
        regionService=RegionService(request)
        message,status=regionService.updateRegion()
        if message is None:
            return Response({"error":"ROLE ID NOT PRESENT"},status=status)
        return Response(message,status=status)

    def delete(self, request:Request)->Response:
        regionService=RegionService(request)
        message,status=regionService.deleteRegion()
        return Response(message,status=status)

@api_view(['GET'])
def fetchFactories(request):
    userRole=parser(request)
    if userRole is None:
        return Response(None, status=status.HTTP_400_BAD_REQUEST)
    factories = Factory.objects.filter(Company=userRole.user_fk.company_fk).values("id","Code","Location","region__Name")
    message = {
        "message": "Factories for the company {} has been fetched successfully".format(
            userRole.user_fk.company_fk.Legalcompanyname
        ),
        "message_body": factories,
    }
    return Response(message, status=status.HTTP_200_OK)


@api_view(["GET"])
def sanitiseRegions(request):
    companies=Company.objects.all()
    regions = ["North","South"]
    for company in companies:
        for region in regions:
            if FactoryRegion.objects.filter(Company=company,Name=region).exists():
                continue
            else:
                FactoryRegion.objects.create(Company=company,Name=region)
    for company in companies:
        factories = Factory.objects.filter(Company=company)
        for factory in factories:
            if factory.Region == "North":
                factoryRegion = FactoryRegion.objects.get(Company=company,Name="North")
                factory.region = factoryRegion
                factory.save()
            elif factory.Region == "South":
                factoryRegion = FactoryRegion.objects.get(Company=company,Name="South")
                factory.region = factoryRegion
                factory.save()
    
    return Response("Regions cleaned")



