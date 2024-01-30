import os
from io import StringIO
import json
from accounts.errors import serialer_error
from accounts.models import HolidayCalendar, Factory
from accounts.serializers import CsvSerializer, HolidayCalendarSerializer
from accounts.Utils.userRoleParser import parser
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from datetime import timedelta, date
from rest_framework.response import Response
import pandas as pd
from django.utils import timezone
from dateutil.parser import parse
import math
from accounts.dateUtils import working_days, convertStringToDate, convertDatestringToDate, pastDateCheck, startEndCheck, weekDayName, pastDateStringCheck, getMonthName, convertDatetimeToHolidayFormat
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse, FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.conf import settings
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from rest_framework.request import Request
from pathlib import Path
class HolidayService:

    def __init__(self, request:Request):
        self.request = request

    def getHolidayCalendar(self):
        if (self.request.query_params == {} or self.request.query_params.get('month') or self.request.query_params.get('year')) and self.request.query_params.get('Factory'):
            message,status=self.getFilteredHolidayCalendar()
        elif self.request.query_params.get("id"):
            message,status=self.getHoliday()
        return message,status

    def createHoliday(self:Request):
        #data = self.request.POST.copy()
        userRole=parser(self.request)
        if userRole is None:
            return None,status.HTTP_400_BAD_REQUEST
        data = self.request.data
        if startEndCheck(data["startDate"],data["endDate"]):
            message = {
                "errorMessage": "End Date needs to be equal or greater than Start Date"
            }
            return message,status.HTTP_400_BAD_REQUEST
        if pastDateCheck(data["startDate"],data["endDate"]):
            message = {
                "errorMessage": "Cannot create Holiday for Past Dates"
            }
            return message,status.HTTP_400_BAD_REQUEST
        yearDate = convertStringToDate(data["startDate"])
        holiday = HolidayCalendar.objects.filter(eventName=data['eventName'],Factory=data["Factory"], startDate__year = yearDate.year)
        if holiday.exists():
            message = {
                "errorMessage": "Holiday with Event Name {} already exists".format(
                    data["eventName"]
                ),
                "message_body": {"existingEventId":holiday.first().id}
            }
            return message,status.HTTP_400_BAD_REQUEST
        if convertStringToDate(data['endDate'])-convertStringToDate(data['startDate']) > timedelta(days=7):
            message = {
                "errorMessage": "Cannot create Holiday for more than 7 days"
            }
            return message,status.HTTP_400_BAD_REQUEST
        serializer = HolidayCalendarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = {
            "message": "Holiday on {} for {} is successfully uploaded".format(
                serializer.data["startDate"],serializer.data["eventName"]
            ),
            "message_body": serializer.data,
        }
        return message,status.HTTP_201_CREATED

    def getHoliday(self:Request):
        try:
            holiday = HolidayCalendar.objects.get(
                id=self.request.query_params.get("id")
            )
            serializer = HolidayCalendarSerializer(holiday)
            message = {
                "message": "Holiday for Event Name {} has been fetched successfully".format(
                    serializer.data["eventName"]
                ),
                "message_body": serializer.data,
            }
            return message,status.HTTP_200_OK

        except HolidayCalendar.DoesNotExist:
            message = {
                "errorMessage": "Holiday with id {} doesn't exist".format(
                        self.request.query_params.get("id")
                    )
            }
            return message,status.HTTP_404_NOT_FOUND

    def getFilteredHolidayCalendar(self:Request):
        userRole=parser(self.request)
        if userRole is None:
            return None,status.HTTP_400_BAD_REQUEST
        try:
            factory = Factory.objects.get(id=self.request.query_params.get('Factory'))
            if self.request.query_params.get('month') or self.request.query_params.get('year'):
                month_str = self.request.query_params.get('month')
                year_str = self.request.query_params.get('year') 

                year = int(year_str) if year_str else None
                month = datetime.strptime(month_str, '%Y-%m') if month_str else None

                filtered_entries = HolidayCalendar.objects.filter(Factory=factory)

                if year is not None:
                    filtered_entries = filtered_entries.filter(Q(startDate__year=year) | Q(endDate__year=year))

                elif month is not None:
                    #TODO : We can update these days based on UI displayable data
                    start_date = month - relativedelta(days=15)
                    end_date = month + relativedelta(months=1, days=15)

                    filtered_entries = filtered_entries.filter(Q(Q(startDate__gte=start_date) & Q(startDate__lte=end_date)) |  Q(Q(endDate__gte=start_date) & Q(endDate__lte=end_date)))

            else:
                today = date.today()
                current_month = datetime(today.year, today.month, 1)
                start_date = current_month - relativedelta(days=15)
                end_date = current_month + relativedelta(months=1, days=15)

                filtered_entries = HolidayCalendar.objects.filter(Q(Factory=factory) & Q(Q(startDate__gte=start_date) & Q(startDate__lte=end_date)) |  Q(Q(endDate__gte=start_date) & Q(endDate__lte=end_date)))

            holidays = filtered_entries#.values("eventName")
            serializer = HolidayCalendarSerializer(holidays,many=True)
            message = {
                "message": "Holiday Calendar for the factory {} has been fetched successfully".format(
                    factory.Code
                ),
                "message_body": {"Holidays":serializer.data}
            }
            return message, status.HTTP_200_OK
        except HolidayCalendar.DoesNotExist:
            message = {
                "message": "Holiday Calendar for the factory {} has been fetched successfully".format(
                    factory.Code
                ),
                "message_body": {"Holidays":[]}
                }
            return message, status.HTTP_200_OK

    def updateHoliday(self:Request):
        userRole=parser(self.request)
        if userRole is None:
            return None,status.HTTP_400_BAD_REQUEST
        try:
            holiday = HolidayCalendar.objects.get(
                id=self.request.query_params.get("id")
            )
            factory = holiday.Factory
            if pastDateStringCheck(str(holiday.startDate),str(holiday.endDate)):
                message = {
                    "errorMessage": "Cannot update Holiday for Past Dates"
                        }
                return message,status.HTTP_400_BAD_REQUEST
            data=self.request.data
            if startEndCheck(data["startDate"],data["endDate"]):
                message = {
                    "errorMessage": "End Date needs to be equal or greater than Start Date"
                }
                return message,status.HTTP_400_BAD_REQUEST
            if pastDateCheck(data["startDate"],data["endDate"]):
                message = {
                    "errorMessage": "Cannot update Holiday with Past Dates"
                }
                return message,status.HTTP_400_BAD_REQUEST
            yearDate = convertStringToDate(data["startDate"])
            holidayCheck = HolidayCalendar.objects.filter(eventName=data['eventName'],Factory=factory, startDate__year = yearDate.year).exclude(id=self.request.query_params.get("id"))
            if holidayCheck.exists():
                message = {
                    "errorMessage": "Holiday with Event Name {} already exists".format(
                        data["eventName"]
                    ),
                    "message_body": {"existingEventId":holidayCheck.first().id}
                }
                return message,status.HTTP_400_BAD_REQUEST
            if convertStringToDate(data['endDate'])-convertStringToDate(data['startDate'])  > timedelta(days=7):
                message = {
                    "errorMessage": "Cannot create Holiday for more than 7 days"
                }
                return message,status.HTTP_400_BAD_REQUEST
            serializer = HolidayCalendarSerializer(
                holiday, data=data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                message = {
                    "message": "Holiday on {} for {} is successfully updated".format(
                        serializer.data["startDate"],serializer.data["eventName"]
                        ),
                    "message_body": serializer.data,
                }
                return message, status.HTTP_201_CREATED
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except HolidayCalendar.DoesNotExist:
            message = {
                "errorMessage": "Holiday with id {} doesn't exist".format(
                        self.request.query_params.get("id")
                    )
            }
            return message,status.HTTP_404_NOT_FOUND

    def deleteHoliday(self:Request):
        try:
            holiday = HolidayCalendar.objects.get(
                id=self.request.query_params.get("id")
            )
            if pastDateStringCheck(str(holiday.startDate),str(holiday.endDate)):
                message = {
                    "errorMessage": "Cannot delete Holiday for Past Dates"
                        }
                return message,status.HTTP_400_BAD_REQUEST
            holiday.delete()
            message = {
                "message": "Holiday with id {} has been Deleted successfully".format(
                    self.request.query_params.get("id")
                )
            }
            return message,status.HTTP_200_OK
        except HolidayCalendar.DoesNotExist:
            message = {
                "errorMessage": "Holiday with id {} doesn't exist".format(
                        self.request.query_params.get("id")
                    )
            }
            return message,status.HTTP_404_NOT_FOUND

    def bulkHolidayUpload(self:Request):
        # Check if the uploaded file is a CSV
        uploaded_file = self.request.FILES.get('csv_file')
        if not uploaded_file:
            return {"error": "No file uploaded"}, status.HTTP_400_BAD_REQUEST

        file_extension = os.path.splitext(uploaded_file.name)[1]
        if file_extension.lower() != '.csv':
            return {"error": "Only CSV files are allowed"}, status.HTTP_400_BAD_REQUEST

        # The file is a valid CSV, proceed with processing
        userRole=parser(self.request)
        if userRole is None:
            return None,status.HTTP_400_BAD_REQUEST
        factory = Factory.objects.get(id=self.request.POST.get("Factory"))
        serializer = CsvSerializer(data=self.request.data)
        try:
            if serializer.is_valid():
                csv_file = self.request.FILES['csv_file']
                csv_data = csv_file.read().decode('utf-8')
                df = pd.read_csv(StringIO(csv_data))
                new_holidays = []
                response={}
                
                for _, row in df.iterrows():
                    (EventName,FromDate,ToDate) = row
                    response[EventName]={'eventName':EventName,
                                        'startDate':FromDate,
                                        'endDate':ToDate,
                                        'errorResponse':''
                                        }
                    # variables =[EventName,FromDate,ToDate]
                    # empty_vars = [var for var in variables if not var]
                    # errorString=""
                    # print(len(empty_vars),empty_vars)
                    # if len(empty_vars)!=0:
                    #     for empty_var in empty_vars:
                    #         response[EventName][empty_var]=''
                    #         errorString=errorString+" "+empty_var
                    #         response[EventName]['errorResponse']=errorString + " is missing"
                    #     continue
                    # print(ToDate)
                    # if empty_vars.__len__!=0:
                    #     if EventName!=EventName:
                    #         response[EventName]['eventName'] =""
                    #         response[EventName]['errorResponse']= "Event Name is missing"
                    #     if FromDate !=FromDate:
                    #         response[EventName]['startDate'] =''
                    #         response[EventName]['errorResponse']= response[EventName]['errorResponse']+" Start Date is missing"
                    #     if ToDate!=ToDate:
                    #         print("dsds")
                    #         response[EventName]['endDate'] =''
                    #         response[EventName]['errorResponse']= response[EventName]['errorResponse']+" End Date is missing"
                    #     continue
                    date_format = "%d/%m/%y"
                    start_date = datetime.strptime(FromDate, date_format)
                    end_date = datetime.strptime(ToDate, date_format)
                    # timeFrame=working_days(start_date.date(), end_date.date())
                    # response[EventName]['timeFrame']=timeFrame
                    if start_date.date() > end_date.date():
                        response[EventName]['errorResponse']= "End Date needs to be equal or greater than Start Date"
                        continue
                    if start_date.date() < date.today() or end_date.date() < date.today():
                        response[EventName]['errorResponse']="Cannot create Holiday for Past Dates"
                        continue
                    #check if the event is already present in the database
                    if end_date-start_date > timedelta(days=7):
                        response[EventName]['errorResponse'] = "Cannot create Holiday for more than 7 days"
                        continue
                    try:
                        event = HolidayCalendar.objects.get(eventName=EventName,Factory=factory,startDate__year=start_date.year)
                        response[EventName]['errorResponse']=EventName + " already exists "
                        continue
                    except:
                        pass
                    # if timeFrame>10:
                    #     response[EventName]['errorResponse']="Timeframe should be less than 10"
                    #     continue
                    # print(response[EventName]['errorResponse'])
                    
                    if (self.request.POST.get("method")=="UPLOAD"):
                        HolidayCalendar.objects.create(eventName=EventName,startDate=start_date,endDate=end_date,Factory=factory)
            else:
                error_response=serialer_error(serializer.errors)
                return error_response , status.HTTP_400_BAD_REQUEST
            
            if (self.request.POST.get("method")=="UPLOAD"):
                message = {
                "message":" Bulk Holidays for the factory {} has been successfully uploaded".format(
                    factory.Code
                ),
                "message_body": {"Holidays":response}
                }
                print(message)
                return message,status.HTTP_201_CREATED
            elif (self.request.POST.get("method")=="ITERATE"):
                message = {
                    "message":" Iterated list of holidays for the factory {} from the uploaded CSV File".format(
                        factory.Code
                    ),
                    "message_body": {"Holidays":response}
                }
                print(message)
                return message,status.HTTP_200_OK   
        except Exception as e:
            print(e)
            return {"errorMessage": "Something went wrong, {} .Please check the sample CSV file and upload accordingly ".format(e)}, status.HTTP_400_BAD_REQUEST    


def downloadPDF(request:Request)->Response:
    userRole=parser(request)
    if userRole is None:
            return None
    try:
        print(request.data)
        response = HttpResponse(content_type='application/pdf',status=status.HTTP_200_OK)
        response['Content-Disposition'] = 'attachment; filename="Holidays.pdf"'

        pdf = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        #table_data = []

        styles = getSampleStyleSheet()
        #cell_style = styles["Normal"]

        factory = Factory.objects.get(id=request.query_params.get('Factory'))
        holidays = HolidayCalendar.objects.all()
        month_str = request.query_params.get('month')
        year_str = request.query_params.get('year') 

        year = int(year_str) if year_str else None
        month = int(month_str.split('-')[1]) if month_str else None

        if year:
            header_text = 'Holiday Calendar of Year ' + year_str
        elif month:
            header_text = 'Holiday Calendar of ' + getMonthName(month_str) + ' ' + month_str.split('-')[0]

        header_style = ParagraphStyle('header_style', fontSize=18, textColor=colors.black, spaceAfter=10, fontName='Helvetica-Bold')
        header_paragraph = Paragraph(header_text, header_style)

        # TODO : Need to get this Image from s3
        logo = Image('accounts/templates/accounts/Inache_Logo_Solid.png', width=100, height=50)
        
        header_table = Table([[header_paragraph, '',logo]], colWidths=[pdf.width - 100, 50, 50])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.white),
            ('LINEABOVE', (0, 1), (-1, 1), 1, colors.white), 
            ('LINEBELOW', (0, 1), (-1, 1), 0, colors.white), 
            ('ALIGN', (-1, 0), (-1, 0), 'RIGHT')
        ]))
        elements.append(header_table)

        elements.append(Spacer(1, 20))

        data = [
            ['S.No', 'Event', 'Date','Day']
        ]
        
        filtered_entries = HolidayCalendar.objects.filter(Factory=factory)

        if year is not None:
            holidays = filtered_entries.filter(Q(startDate__year=year) | Q(endDate__year=year))

        elif month is not None:
            year = int(month_str.split('-')[0])
            holidays = filtered_entries.filter(Q(startDate__year=year) & Q(Q(startDate__month=month) | Q(endDate__month=month)))

        count=0
        for item in holidays:
            count +=1
            data.append([count,item.eventName, convertDatetimeToHolidayFormat(item.startDate) + "  -  " + convertDatetimeToHolidayFormat(item.endDate), weekDayName(item.startDate,item.endDate)]) 

        # for row in data:
        #     table_row = []
        #     for cell in row:
        #         if isinstance(cell, str) and "," in cell:
        #             cell_text = cell.replace(", ", "<br/>")
        #             cell_obj = Paragraph(cell_text, cell_style)
        #         else:
        #             cell_obj = cell
        #         table_row.append(cell_obj)
        #     table_data.append(table_row)

        #table = Table(data)
        #table = Table(data, colWidths=[pdf.width / len(data[0])] * len(data[0]))

        total_width = pdf.width
        column_widths = [0.1, 0.2, 0.4, 0.4] 
        actual_widths = [total_width * width for width in column_widths]
        table = Table(data, colWidths=actual_widths)

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.aliceblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        ]))
        elements.append(table)

        pdf.build(elements)

        return response
    
    except:
        message = {
            "errorMessage": "Ensure either Year or Month was given in the Right Format"
        }
        return Response(message,status=status.HTTP_404_NOT_FOUND)  

#TODO: Need to depreciate after implementing s3 
def holidayCSV(request:Request):
    #from the given path, opens the csv, create a fileresponse and return it
    path_obj = Path(settings.BASE_DIR)
    new_path = str(path_obj.parent)
    csv_path = os.path.join(new_path, 'accounts', 'templates', 'accounts', 'Bulk Holiday Upload Template.csv')
    csv_file = open(csv_path, 'rb')
    response = FileResponse(csv_file, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Bulk Holiday Upload Template.csv"'

    return response
