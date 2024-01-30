from accounts.permissions import HasGroupPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.Service.holidayService import HolidayService, downloadPDF, holidayCSV
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework import status

class HolidayDetails(APIView):
    # permission_classes = [
    #     #  hasholiday_permission
        
    # ]
    permission_classes = [HasGroupPermission]
    required_groups = {
        "GET": ["SUPER_ADMIN", "FACTORY_ADMIN", "CR", "CT", "REGIONAL_ADMIN"],
        "PATCH":["SUPER_ADMIN","REGIONAL_ADMIN"],
        "POST": ["SUPER_ADMIN","REGIONAL_ADMIN"],
        "DELETE": ["SUPER_ADMIN","REGIONAL_ADMIN"],
    }
    model = "holidaycalendar"
   
    def get(self, request:Request)->Response:
        holidayService = HolidayService(request)
        message,status=holidayService.getHolidayCalendar()
        if message is None:
            return Response({"error":"ROLE ID NOT PRESENT"},status=status)
        return Response(message,status=status)
    
    def post(self, request:Request)->Response:
        holidayService=HolidayService(request)
        message,status=holidayService.createHoliday()
        if message is None:
            return Response({"error":"ROLE ID NOT PRESENT"},status=status)
        return Response(message,status=status)

    def patch(self, request:Request)->Response:
        holidayService=HolidayService(request)
        message,status=holidayService.updateHoliday()
        if message is None:
            return Response({"error":"ROLE ID NOT PRESENT"},status=status)
        return Response(message,status=status)

    def delete(self, request:Request)->Response:
        holidayService=HolidayService(request)
        message,status=holidayService.deleteHoliday()
        return Response(message,status=status)

@api_view(['POST'])
def bulkHolidayUpload(request:Request)->Response:
    bulkHolidayUpload.required_groups = {
        "POST": ["SUPER_ADMIN","REGIONAL_ADMIN"],
    }
    bulkHolidayUpload.model = "holidaycalendar"
    # permission_classes =[hasholiday_permission]
    holidayService=HolidayService(request)
    message,\
        status=holidayService.bulkHolidayUpload()
    if message is None:
            return Response({"error":"ROLE ID NOT PRESENT"},status=status)
    return Response(message,status=status)

@api_view(["GET"])
def downloadHoliday(request:Request)->Response:
    message = downloadPDF(request)
    if message is None:
            return Response({"error":"ROLE ID NOT PRESENT"},status=status.HTTP_400_BAD_REQUEST)
    return message


@api_view(["GET"])
def bulkUploadCSV(request:Request)->Response:
    message = holidayCSV(request)
    return message


