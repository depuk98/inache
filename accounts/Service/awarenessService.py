from accounts.models import AwarenessProgram, Factory
from accounts.serializers import AwarenessProgramSerializer
from accounts.Utils.userRoleParser import parser
from rest_framework import  status
from datetime import timedelta, date
from calendar import SATURDAY
import datetime
from django.db.models import Q
from accounts.dateUtils import programCheck, last_three_working_days, first_two_working_days
from rest_framework.request import Request
from django.db.models.query import QuerySet
from accounts.utils import current_time

class AwarenessService:

    def __init__(self, request:Request):
        self.request = request

    def getAwarenessProgram(self:Request):
        if (self.request.query_params == {} or self.request.query_params.get('month') or self.request.query_params.get('quarter') or self.request.query_params.get('half') or self.request.query_params.get('year')) and self.request.query_params.get('Factory'):
            message,status=self.getFilteredAwarenessProgram()
        elif self.request.query_params.get("programNumber"):
            message,status=self.getProgramByNumber()
        return message, status
    
    def createAwarenessProgram(self:Request):
        print(self.request.data,"requestdatapure")
        data=self.request.data.copy()
        # data = self.request.data
        userRole=parser(self.request)
        if userRole is None:
            return None,status.HTTP_400_BAD_REQUEST
        factory = Factory.objects.get(id=data["Factory"])
        data["uploadedBy"]=self.request.user.user_name
        serializer = AwarenessProgramSerializer(data=data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        awareness = serializer.save()
        Number = (
                "APN" + factory.Code + str(awareness.id)
        )
        awareness.programNumber = Number
        
        programStatus=getAwarenessProgramStatus(self.request,awareness,factory)
        
        awareness.programStatus=programStatus
        awareness.save()   
        message = {
            "message": "Great!! Awareness Program {} is uploaded successfully".format(
                Number
            ),
            "message_body": serializer.data,
        }
        return message,status.HTTP_201_CREATED
    def getProgramByNumber(self:Request):
        try:
            program = AwarenessProgram.objects.get(
                programNumber=self.request.query_params.get("programNumber")
            )
            serializer = AwarenessProgramSerializer(program)
            message = {
                "message": "Awareness Program with Program Number {} has been fetched successfully".format(
                    serializer.data["programNumber"]
                ),
                "message_body": serializer.data,
            }
            return message,status.HTTP_200_OK
        except AwarenessProgram.DoesNotExist:
            
            return {
                    "errorMessage": "Awareness Program with program Number {} doesn't exist".format(
                        self.request.query_params.get("programNumber")
                    )
                },status.HTTP_404_NOT_FOUND
    def getFilteredAwarenessProgram(self:Request):
        userRole=parser(self.request)
        if userRole is None:
            return None,status.HTTP_400_BAD_REQUEST
        try:
            factory = Factory.objects.get(id=self.request.query_params.get('Factory'))
            if self.request.query_params.get('month') or self.request.query_params.get('quarter') or self.request.query_params.get('half') or self.request.query_params.get('year'):
                half_str = self.request.query_params.get('half')
                quarter_str = self.request.query_params.get('quarter') 
                month_str = self.request.query_params.get('month')
                year_str = self.request.query_params.get('year') 

                year = int(year_str) if year_str else None
                half_num = int(half_str[-1]) if half_str else None
                quarter_num = int(quarter_str[-1]) if quarter_str else None
                month = int(month_str.split('-')[1]) if month_str else None

                filtered_entries = AwarenessProgram.objects.filter(Factory=factory)

                if year is not None:
                    filtered_entries = filtered_entries.filter(Date__year=year)
                    months = list(range(1, 13)) 

                elif half_num is not None:
                    year = int(half_str.split('-')[0])
                    filtered_entries = filtered_entries.filter(Date__year=year)

                    if half_num == 1:
                        start_date = datetime.datetime(year, 1, 1)
                        end_date = datetime.datetime(year, 6, 30) 
                        months = list(range(1, 7)) 
                    else:
                        start_date = datetime.datetime(year, 7, 1)
                        end_date = datetime.datetime(year, 12, 31) 
                        months = list(range(7, 13)) 

                    filtered_entries = filtered_entries.filter(Q(Date__gte=start_date) & Q(Date__lte=end_date))

                elif quarter_num is not None:
                    year = int(quarter_str.split('-')[0])
                    filtered_entries = filtered_entries.filter(Date__year=year)

                    if quarter_num == 1:
                        start_date = datetime.datetime(year, 1, 1)
                        end_date = datetime.datetime(year, 3, 31) 
                        months = list(range(1, 4))
                    elif quarter_num == 2:
                        start_date = datetime.datetime(year, 4, 1)
                        end_date = datetime.datetime(year, 6, 30) 
                        months = list(range(4, 7))
                    elif quarter_num == 3:
                        start_date = datetime.datetime(year, 7, 1)
                        end_date = datetime.datetime(year, 9, 30) 
                        months = list(range(7, 10))
                    else:
                        start_date = datetime.datetime(year, 10, 1)
                        end_date = datetime.datetime(year, 12, 31) 
                        months = list(range(10, 13))  

                    filtered_entries = filtered_entries.filter(Q(Date__gte=start_date) & Q(Date__lte=end_date))

                elif month is not None:
                    year = int(month_str.split('-')[0])
                    months = [month]
                    filtered_entries = filtered_entries.filter(Q(Date__year=year) & Q(Date__month=month))

                Status = {}
                count=0
                for month_num in months:
                    check = filtered_entries.filter(Q(Date__year=year) & Q(Date__month=month_num))
                    if check.exists():
                        count +=1
                        month_dict = check.latest("id").programStatus
                    else:
                        month_dict = {"Required":4,"Conducted":0,"Pending":4}
                    if Status == {}:
                        Status = month_dict
                    else:
                        for key in Status.keys():
                            Status[key] = Status[key] + month_dict[key]
                if count==0:
                        if [current_time().month] == months:
                            Status = {"Required":factory.requiredAwarenessProgram,"Conducted":0,"Pending":factory.requiredAwarenessProgram}

            else:
                start_date = date.today().replace(day=1)
                end_date = date.today() 

                filtered_entries = AwarenessProgram.objects.filter(Q(Factory=factory) & Q(Date__date__gte=start_date) & Q(Date__date__lte=end_date))
                Status = filtered_entries.latest("id").programStatus


            programs = filtered_entries.values("programNumber","programName","Date","uploadedBy","participants","uploadedAt","Breached").order_by("-uploadedAt")
            message = {
                "message": "Awareness Programs for the factory {} has been fetched successfully".format(
                    factory.Code
                ),
                "message_body": {"Programs":programs, "Status":Status}
            }
            # return Response(message, status=status.HTTP_200_OK)
            return message, status.HTTP_200_OK
        except AwarenessProgram.DoesNotExist:
            message = {
                "message": "Awareness Programs for the factory {} has been fetched successfully".format(
                    factory.Code
                ),
                "message_body": {"Programs":[], "Status":{"Required":factory.requiredAwarenessProgram,"Conducted":0,"Pending":factory.requiredAwarenessProgram}}
                }
            return message, status.HTTP_200_OK


def calendarFunction(request:Request):
    timestamp_str = request.data["Date"]
    factory = Factory.objects.get(id=request.data["Factory"])
    format_str = '%Y-%m-%d %H:%M:%S.%f%z'
    Date_datetime = datetime.datetime.strptime(timestamp_str, format_str)
    Date = Date_datetime.date()
    Today = datetime.datetime.today().date()
    working_days = last_three_working_days(Date.year,Date.month,factory)
    grace_days = first_two_working_days(Today.year,Today.month,factory)
    if Date.month < Today.month:
        if (Date in working_days) and (Today in grace_days):
            return {'Delay Reason Required': False}
        else:
            return {'Delay Reason Required': True}
    else:
        return {'Delay Reason Required': False}

def updateStatus(request:Request,currentpgms:QuerySet,factory)->dict:
    userRole=parser(request)
    if userRole is None:
            return None,status.HTTP_400_BAD_REQUEST
    print("check",currentpgms.values_list())
    if currentpgms.exists() == False:
        pending=max(factory.requiredAwarenessProgram-(currentpgms.count()+1),0)
        Status = {"Required":factory.requiredAwarenessProgram,"Conducted":currentpgms.count()+1,"Pending":pending}
    else:
        pgmStatus = currentpgms.latest("id").programStatus
        pending=max(pgmStatus['Required']-(currentpgms.count()+1),0)

        Status = {"Required":pgmStatus['Required'],"Conducted":currentpgms.count()+1,"Pending":pending}
    return Status

def getAwarenessProgramStatus(request:Request,awareness,factory):
    userRole=parser(request)
    if userRole is None:
            return None,status.HTTP_400_BAD_REQUEST
    timestamp_str = request.data["Date"]
    format_str = '%Y-%m-%d %H:%M:%S.%f%z'
    conductedDate = datetime.datetime.strptime(timestamp_str, format_str)
    conductedMonth = conductedDate.month
    currentMonth =  current_time().month
    #if the awareness program has been uploaded within the same month
    if conductedMonth == currentMonth:
        startDate = date.today().replace(day=1)
        endDate = date.today()
        currentpgms = AwarenessProgram.objects.filter(
                        Date__date__gte=startDate, Date__date__lte=endDate, Factory=factory
                    ).exclude(id=awareness.id)
        Status = updateStatus(request,currentpgms,factory)

    else:
        currentpgms = AwarenessProgram.objects.filter(
            Date__year=conductedDate.year, Date__month=conductedMonth, Factory=factory
        ).exclude(id=awareness.id)
        #if the awareness program is uploaded in next month but within the grace period
        if programCheck(conductedDate, factory):
            Status = updateStatus(request,currentpgms)

        #if the awareness programs has breached the grace period too
        else:
            if currentpgms.exists() == False:
                awareness.Breached = True
                Status = {"Required":factory.requiredAwarenessProgram,"Conducted":0,"Pending":factory.requiredAwarenessProgram}
            else:
                awareness.Breached = True
                pgmStatus = currentpgms.latest("id").programStatus
                Status = pgmStatus

    return Status