from accounts.models import FactoryRegion, Factory, BaseUserModel, UserRoleFactory
from accounts.serializers import FactoryRegionSerializer
from accounts.Utils.userRoleParser import parser
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.request import Request
from accounts.utils import current_time

class RegionService:

    def __init__(self, request:Request):
        self.request = request

    def getFactoryRegion(self):
        if self.request.query_params == {}:
            message,status=self.getRegions()
        elif self.request.query_params.get("id"):
            message,status=self.getRegion()
        return message,status

    def getRegion(self:Request):
        userRole=parser(self.request)
        if userRole is None:
            return None,status.HTTP_400_BAD_REQUEST
        try:
            region = FactoryRegion.objects.get(
                id=self.request.query_params.get("id")
            )
            company = userRole.user_fk.company_fk
            serializer = FactoryRegionSerializer(region)
            result = serializer.data
            result["Factories"]=Factory.objects.filter(Company=company,region=serializer.data["id"],is_active=True).values("id","Code","Location","region__Name")
            result["remainingFactories"]=Factory.objects.filter(Company=company,is_active=True).exclude(region=serializer.data["id"]).values("id","Code","Location","region__Name")
            message = {
                "message": "Region named {} has been fetched successfully".format(
                    serializer.data["Name"]
                ),
                "message_body": result,
            }
            return message,status.HTTP_200_OK

        except FactoryRegion.DoesNotExist:
            message = {
                "errorMessage": "Region with id {} doesn't exist".format(
                        self.request.query_params.get("id")
                    )
            }
            return message,status.HTTP_404_NOT_FOUND

    def getRegions(self:Request):
        userRole=parser(self.request)
        if userRole is None:
            return None,status.HTTP_400_BAD_REQUEST
        try:
            company = userRole.user_fk.company_fk
            regions = FactoryRegion.objects.filter(Company=company).order_by("-last_modified")
            serializer = FactoryRegionSerializer(regions,many=True)
            for item in serializer.data:
                item["Factories"]=Factory.objects.filter(Company=company,region=item["id"],is_active=True).values_list("Code")
                item["regionaAdmin"]= UserRoleFactory.objects.filter(region_fk=item["id"],role__role="REGIONAL_ADMIN",is_active=True,user_fk__is_active=True,user_fk__company_fk=company).values_list("user_fk__user_name")
            message = {
                "message": "Regions for Company {} been fetched successfully".format(
                    company
                ),
                "message_body": {"Regions":serializer.data}
            }
            return message, status.HTTP_200_OK
        except FactoryRegion.DoesNotExist:
            message = {
                "message": "Regions for Company {} have been fetched successfully".format(
                    company
                ),
                "message_body": {"Regions":[]}
                }
            return message, status.HTTP_200_OK

    def createRegion(self:Request):
        userRole=parser(self.request)
        if userRole is None:
            return None,status.HTTP_400_BAD_REQUEST
        data = self.request.data
        data["Company"]=userRole.user_fk.company_fk.id
        region = FactoryRegion.objects.filter(Name=data['Name'],Company=userRole.user_fk.company_fk)
        if region.exists():
            message = {
                "errorMessage": "Region with Name {} already exists".format(
                    data["Name"]
                ),
                "message_body": {"existingRegionId":region.first().id}
            }
            return message,status.HTTP_400_BAD_REQUEST
        serializer = FactoryRegionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {
            "message": "Region named {} is successfully created".format(
                serializer.data["Name"]
            ),
            "message_body": serializer.data,
        }
        return message,status.HTTP_201_CREATED

    def updateRegion(self:Request):
        userRole=parser(self.request)
        if userRole is None:
            return None,status.HTTP_400_BAD_REQUEST
        try:
            region = FactoryRegion.objects.get(
                id=self.request.query_params.get("id")
            )
            if self.request.query_params.get("operation") == "name":
                data=self.request.data
                regionCheck = FactoryRegion.objects.filter(Name=data['Name'],Company=userRole.user_fk.company_fk).exclude(id=self.request.query_params.get("id"))
                if regionCheck.exists():
                    message = {
                        "errorMessage": "Region with Name {} already exists".format(
                            data["Name"]
                        ),
                        "message_body": {"existingRegionId":regionCheck.first().id}
                    }
                    return message,status.HTTP_400_BAD_REQUEST
            elif self.request.query_params.get("operation") == "transfer":
                factories = self.request.data["factories"]
                data={}
                for item in factories:
                    factory = Factory.objects.get(id=item)
                    factory.region = region
                    factory.save()
            data["last_modified"] = current_time()
            serializer = FactoryRegionSerializer(
                region, data=data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = {
                    "message": "Region is successfully updated",
                    "message_body": serializer.data,
                }
                return message, status.HTTP_201_CREATED
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except FactoryRegion.DoesNotExist:
            message = {
                "errorMessage": "Region with id {} doesn't exist".format(
                        self.request.query_params.get("id")
                    )
            }
            return message,status.HTTP_404_NOT_FOUND

    def deleteRegion(self:Request):
        try:
            region = FactoryRegion.objects.get(
                id=self.request.query_params.get("id")
            )
            name=region.Name
            if Factory.objects.filter(region=self.request.query_params.get("id")).exists():
                message = {
                    "errorMessage": "Cannot delete Region as it is associated with Factories"
                        }
                return message,status.HTTP_400_BAD_REQUEST
            region.delete()
            message = {
                "message": "Region with Name {} has been Deleted successfully".format(
                    name
                )
            }
            return message,status.HTTP_200_OK
        except FactoryRegion.DoesNotExist:
            message = {
                "errorMessage": "Region with id {} doesn't exist".format(
                        self.request.query_params.get("id")
                    )
            }
            return message,status.HTTP_404_NOT_FOUND


