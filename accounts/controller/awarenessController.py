from accounts.Service.awarenessService import AwarenessService, calendarFunction
from rest_framework.response import Response
from django.db import models,transaction
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.permissions import OR
from accounts.permissions import HasGroupPermission, hasawarenesspermission

class ProgramDetails(APIView):
    permission_classes = [( hasawarenesspermission|HasGroupPermission)]
    required_groups = {
        "GET": ["SUPER_ADMIN", "FACTORY_ADMIN", "REGIONAL_ADMIN",],
        # "PATCH":["SUPER_ADMIN",],
        "POST": ["SUPER_ADMIN",],
        # "DELETE": ["SUPER_ADMIN"],
    }
    model = "awarenessprogram"
    def get(self, request:Request)->Response:
        awarenessService=AwarenessService(request)
        message,status=awarenessService.getAwarenessProgram()
        if message is None:
            return Response({"error":"ROLE ID NOT PRESENT"},status=status)
        return Response(message,status=status)
    
    @transaction.atomic
    def post(self, request:Request)->Response:
        awarenessService=AwarenessService(request)
        message,status=awarenessService.createAwarenessProgram()
        if message is None:
            return Response({"error":"ROLE ID NOT PRESENT"},status=status)
        return Response(message,status=status)


@api_view(["POST"])
def calendarCheck(request:Request)->Response:
    message = calendarFunction(request)
    return Response(message)


        
