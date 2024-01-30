
from rest_framework.decorators import api_view
from InacheBackend.DynamoDB.config_single import add_user_session_data, scan_dynamodb_table, get_user_session_by_email , get_user_session_data, generate_session_id
from InacheBackend.DynamoDB.config import (
    add_user_metrics, 
    add_user_roles, 
    add_page_metrics, 
    add_event_metrics, 
    scan_table, 
    get_user_metric, 
    get_user_roles, 
    get_page_visits, 
    get_event_metrics,
    create_dynamodb_table,
    create_dynamodb_table_with_gsi,
    delete_table,
    calculate_active_users,
    get_average_session_duration,
    get_average_pages_per_session,
    calculate_bounce_rate,
    count_role_logins,
    calculate_user_retention,
    calculate_churn_rate
)
from rest_framework.response import Response
from rest_framework import status
from accounts.dateUtils import convertDatestringToDate, analyticsStartEndCheck, futureDateStringCheck
import pandas as pd
from datetime import datetime, timedelta
from django.http import HttpResponse
import io



@api_view(["POST"])
def uploadMetrics(request):
    session_id = generate_session_id()
    response = add_user_session_data(request.data, session_id)
    # return Response("success, metrics added with session id: " + session_id)
    message = {
                    "message": "success, metrics added with session id: {}".format(
                        session_id
                    )
                }
    return Response(message, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def getAllMetrics(request):
    response = scan_dynamodb_table()
    return Response(response)

@api_view(["GET"])
def getEmailMetrics(request):
    email = request.query_params.get('email')
    response = get_user_session_by_email(email)
    return Response(response)

@api_view(["GET"])
def getUserMetric(request):
    email = request.query_params.get('email')
    sessionId = request.query_params.get('sessionId')
    response = get_user_session_data(email, sessionId)
    return Response(response)


################################################################################################


@api_view(["POST"])
def uploadUserMetrics(request):
    email = request.data['userMetrics']['email']
    sessionId = generate_session_id()
    add_user_metrics(request.data, sessionId)
    add_user_roles(email, sessionId, request.data['userRoles'])
    add_page_metrics(email, sessionId, request.data['pageMetrics'])
    add_event_metrics(email, sessionId, request.data['eventMetrics'])
    message = {
                    "message": "success, metrics added with session id: {}".format(
                        sessionId
                    )
                }
    return Response(message, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def getTableMetrics(request):
    table_name = request.query_params.get('tableName')
    response = scan_table(table_name)
    return Response(response)


@api_view(["GET"])
def getMetric(request):
    email = request.query_params.get('email')
    sessionId = request.query_params.get('sessionId')
    user_metrics = get_user_metric(email, sessionId)
    user_roles = get_user_roles(email, sessionId)
    page_visits = get_page_visits(email, sessionId)
    event_metrics = get_event_metrics(email, sessionId)
    total_metrics = {"User Metrics":user_metrics, "User Roles":user_roles, "Page Visits":page_visits, "Event Metrics":event_metrics}
    return Response(total_metrics)


@api_view(["GET"])
def createMetricTables(request):
    gsi = [
    {
        'IndexName': 'EmailSessionIndex',
        'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'},{'AttributeName': 'sessionId', 'KeyType': 'RANGE'}],
        'Projection': {'ProjectionType': 'ALL'},
        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    }
]
    user_metrics_table = create_dynamodb_table(
        'UserMetrics', 
        [{'AttributeName': 'email','KeyType': 'HASH' },{'AttributeName': 'sessionId','KeyType': 'RANGE' }], 
        [{'AttributeName': 'email','AttributeType': 'S'},{'AttributeName': 'sessionId','AttributeType': 'S'}],
        {'ReadCapacityUnits': 10,'WriteCapacityUnits': 10})
    user_roles_table = create_dynamodb_table_with_gsi(
        'UserRoles', 
        [{'AttributeName': 'roleID','KeyType': 'HASH' },{'AttributeName': 'sessionId','KeyType': 'RANGE' }], 
        [{'AttributeName': 'roleID','AttributeType': 'N'},{'AttributeName': 'sessionId','AttributeType': 'S'},{'AttributeName': 'email','AttributeType': 'S' }],
        {'ReadCapacityUnits': 10,'WriteCapacityUnits': 10},
        gsi)
    page_metrics_table = create_dynamodb_table_with_gsi(
        'PageMetrics', 
        [{'AttributeName': 'pageName','KeyType': 'HASH' },{'AttributeName': 'sessionId','KeyType': 'RANGE' }], 
        [{'AttributeName': 'pageName','AttributeType': 'S'},{'AttributeName': 'sessionId','AttributeType': 'S'},{'AttributeName': 'email','AttributeType': 'S' }],
        {'ReadCapacityUnits': 10,'WriteCapacityUnits': 10},
        gsi)
    event_metrics_table = create_dynamodb_table_with_gsi(
        'EventMetrics', 
        [{'AttributeName': 'actionType','KeyType': 'HASH' },{'AttributeName': 'sessionId','KeyType': 'RANGE' }], 
        [{'AttributeName': 'actionType','AttributeType': 'S'},{'AttributeName': 'sessionId','AttributeType': 'S'},{'AttributeName': 'email','AttributeType': 'S' }],
        {'ReadCapacityUnits': 10,'WriteCapacityUnits': 10},
        gsi)
    message = {
        "message": (
            "success, Metric tables were created. \n"
            "UserMetrics Table status: {}, \n"
            "UserRoles Table status: {}, \n"
            "PageMetrics Table status: {}, \n"
            "EventMetrics Table status: {}"
        ).format(
            user_metrics_table.table_status,
            user_roles_table.table_status,
            page_metrics_table.table_status,
            event_metrics_table.table_status
        )
    }
    return Response(message, status=status.HTTP_201_CREATED)




@api_view(["GET"])
def deleteTableMetrics(request):
    table_name = request.query_params.get('tableName')
    response = delete_table(table_name)
    message = {
                "message": "Table with TableName {} has been Deleted successfully".format(
                    request.query_params.get("tableName")
                )
            }
    return Response(message, status=status.HTTP_204_NO_CONTENT)



@api_view(["GET"])
def getActiveUserMetrics(request):
    dau = calculate_active_users('D')
    wau = calculate_active_users('W')
    mau = calculate_active_users('M')
    return Response(f"DAU: {dau}, WAU: {wau}, MAU: {mau}")


@api_view(["GET"])
def getAverageSessionDuration(request):
    startDate = request.query_params.get('startDate')
    endDate = request.query_params.get('endDate')
    if analyticsStartEndCheck(startDate,endDate):
            message = {
                "errorMessage": "End Date needs to be equal or greater than Start Date"
            }
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    if futureDateStringCheck(startDate,endDate):
            message = {
                "errorMessage": "Start Date or End Date cannot be in the future"
            }
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    start_date = convertDatestringToDate(startDate).date()
    end_date = convertDatestringToDate(endDate).date()
    average_duration = get_average_session_duration(start_date, end_date)
    return Response(f"Average Session Duration: {average_duration} minutes")


@api_view(["GET"])
def getAveragePages(request):
    average_pages = get_average_pages_per_session()
    return Response(f"Average Pages per Session: {average_pages}")


@api_view(["GET"])
def getBounceRate(request):
    bounce_rate = calculate_bounce_rate()
    return Response(f"Bounce Rate: {bounce_rate}%")


@api_view(["GET"])
def getRoleLogins(request):
    role_logins_count = count_role_logins()
    return Response(f"Role Logins Count: {role_logins_count}")


@api_view(["GET"])
def getUserRetention(request):
    start_date = request.query_params.get('startDate')
    end_date = request.query_params.get('endDate')
    if analyticsStartEndCheck(start_date,end_date):
            message = {
                "errorMessage": "End Date needs to be equal or greater than Start Date"
            }
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    if futureDateStringCheck(start_date,end_date):
            message = {
                "errorMessage": "Start Date or End Date cannot be in the future"
            }
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    retention = calculate_user_retention(start_date, end_date)
    return Response(f"User Retention Percentage: {retention}%")


@api_view(["GET"])
def getChurnRate(request):
    start_date = request.query_params.get('startDate')
    end_date = request.query_params.get('endDate')
    if analyticsStartEndCheck(start_date,end_date):
            message = {
                "errorMessage": "End Date needs to be equal or greater than Start Date"
            }
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    if futureDateStringCheck(start_date,end_date):
            message = {
                "errorMessage": "Start Date or End Date cannot be in the future"
            }
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
    churn_rate = calculate_churn_rate(start_date, end_date)
    return Response(f"Churn Rate: {churn_rate}%")




@api_view(["GET"])
def export_analytics_to_csv(request):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    analytics_data = {
        "DAU": calculate_active_users('D'),
        "WAU": calculate_active_users('W'),
        "MAU": calculate_active_users('M'),
        "Average Session Duration": get_average_session_duration(start_date.date(), end_date.date()),
        "Average Pages per Session": get_average_pages_per_session(),
        "Bounce Rate": calculate_bounce_rate(),
        "Role Logins Count": count_role_logins(),
        "User Retention Percentage": calculate_user_retention(start_date_str, end_date_str),
        "Churn Rate": calculate_churn_rate(start_date_str, end_date_str)
    }

    df = pd.DataFrame([analytics_data])

    csv_file = io.StringIO()
    df.to_csv(csv_file, index=False)
    csv_file.seek(0)
    
    response = HttpResponse(csv_file.read(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=analytics_report.csv'

    return response







