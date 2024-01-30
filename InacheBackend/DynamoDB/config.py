import boto3
from boto3.dynamodb.conditions import Key
import uuid
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse
import numpy as np
from collections import defaultdict
# from decouple import config
import os
from django.conf import settings

def get_dynamodb_local():
    return boto3.resource('dynamodb', 
                          region_name='localhost', 
                          endpoint_url='http://localhost:8001', 
                          aws_access_key_id='fakeMyKeyId', 
                          aws_secret_access_key='fakeSecretAccessKey')


def get_dynamodb():
    return boto3.resource(
        'dynamodb',
        aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
        )

# def get_dynamodb():
#     return boto3.resource('dynamodb')

if os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.dev':
    dynamodb = get_dynamodb_local() 
elif os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.staging':
    dynamodb = get_dynamodb() 
elif os.environ.get('DJANGO_SETTINGS_MODULE') == 'InacheBackend.settings.production':
    dynamodb = get_dynamodb() 




def create_dynamodb_table(table_name, key_schema, attribute_definitions, provisioned_throughput):
    # dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput=provisioned_throughput
    )

    return table

table_name = 'UserMetrics'
key_schema = [
    {
        'AttributeName': 'email',
        'KeyType': 'HASH' 
    },
    {
        'AttributeName': 'sessionId',
        'KeyType': 'RANGE'  
    }
]
attribute_definitions = [
    {
        'AttributeName': 'email',
        'AttributeType': 'S'  
    },
    {
        'AttributeName': 'sessionId',
        'AttributeType': 'S' 
    }

]
provisioned_throughput = {
    'ReadCapacityUnits': 10,
    'WriteCapacityUnits': 10
}

# user_metrics_table = create_dynamodb_table(table_name, key_schema, attribute_definitions, provisioned_throughput)

def create_dynamodb_table_with_gsi(table_name, key_schema, attribute_definitions, provisioned_throughput, gsi):
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput=provisioned_throughput,
        GlobalSecondaryIndexes=gsi
    )
    return table


table_name = 'UserRoles'
key_schema = [
    {
        'AttributeName': 'roleID',
        'KeyType': 'HASH' 
    },
    {
        'AttributeName': 'sessionId',
        'KeyType': 'RANGE'  
    }
]
attribute_definitions = [
    {
        'AttributeName': 'roleID',
        'AttributeType': 'N'  
    },
    {
        'AttributeName': 'sessionId',
        'AttributeType': 'S' 
    },
    {
        'AttributeName': 'email',
        'AttributeType': 'S' 
    }

]
provisioned_throughput = {
    'ReadCapacityUnits': 10,
    'WriteCapacityUnits': 10
}

gsi = [
    {
        'IndexName': 'EmailSessionIndex',
        'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'},{'AttributeName': 'sessionId', 'KeyType': 'RANGE'}],
        'Projection': {'ProjectionType': 'ALL'},
        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    }
]

# user_roles_table = create_dynamodb_table_with_gsi(table_name, key_schema, attribute_definitions, provisioned_throughput, gsi)


table_name = 'PageMetrics'
key_schema = [
    {
        'AttributeName': 'pageName',
        'KeyType': 'HASH' 
    },
    {
        'AttributeName': 'sessionId',
        'KeyType': 'RANGE'  
    }
]
attribute_definitions = [
    {
        'AttributeName': 'pageName',
        'AttributeType': 'S'  
    },
    {
        'AttributeName': 'sessionId',
        'AttributeType': 'S' 
    },
    {
        'AttributeName': 'email',
        'AttributeType': 'S' 
    }

]
provisioned_throughput = {
    'ReadCapacityUnits': 10,
    'WriteCapacityUnits': 10
}

gsi = [
    {
        'IndexName': 'EmailSessionIndex',
        'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'},{'AttributeName': 'sessionId', 'KeyType': 'RANGE'}],
        'Projection': {'ProjectionType': 'ALL'},
        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    }
]

# page_metrics_table = create_dynamodb_table_with_gsi(table_name, key_schema, attribute_definitions, provisioned_throughput, gsi)


table_name = 'EventMetrics'

key_schema = [
    {'AttributeName': 'actionType', 'KeyType': 'HASH'}, 
    {'AttributeName': 'sessionId', 'KeyType': 'RANGE'}  
]
attribute_definitions = [
    {'AttributeName': 'actionType', 'AttributeType': 'S'},
    {'AttributeName': 'sessionId', 'AttributeType': 'S'},
    {'AttributeName': 'email', 'AttributeType': 'S'}  
]
provisioned_throughput = {
    'ReadCapacityUnits': 10,
    'WriteCapacityUnits': 10
}

gsi = [
    {
        'IndexName': 'EmailSessionIndex',
        'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'},{'AttributeName': 'sessionId', 'KeyType': 'RANGE'}],
        'Projection': {'ProjectionType': 'ALL'},
        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    }
]

# event_metrics_table = create_dynamodb_table_with_gsi(table_name, key_schema, attribute_definitions, provisioned_throughput, gsi)


# print("Table status:", user_metrics_table.table_status)
# print("Table status:", user_roles_table.table_status)
# print("Table status:", page_metrics_table.table_status)
# print("Table status:", event_metrics_table.table_status)

def generate_session_id():
    return str(uuid.uuid4())

def add_user_metrics(session_data, sessionId):
    table = dynamodb.Table('UserMetrics')
    item = {
        'email': session_data['userMetrics']['email'],
        'sessionId': sessionId, 
        'userID': session_data['userMetrics']['userID'],
        'loginTimestamp': session_data['userMetrics']['loginTimestamp'],
        'logoutType': session_data['userMetrics']['logoutType'],
        'logoutTimestamp': session_data['userMetrics']['logoutTimestamp'],
        'sessionDuration': session_data['userMetrics']['sessionDuration']
    }
    table.put_item(Item=item)


def add_user_roles(email, sessionId, roles_data):
    table = dynamodb.Table('UserRoles')
    for role_data in roles_data:
        item = {
            'email': email,
            'sessionId': sessionId,
            'role': role_data['role'],
            'roleID': role_data['roleID'],
            'factoryCode': role_data.get('factoryCode', ''),
            'region': role_data.get('region', ''),
            'company': role_data.get('company', ''),
            'roleActive': role_data['roleActive']
        }
        table.put_item(Item=item)


def add_page_metrics(email, sessionId, page_metrics_data):
    table = dynamodb.Table('PageMetrics')
    for page, timestamps in page_metrics_data['pageVisitTimestamps'].items():
        item = {
            'email': email,
            'sessionId': sessionId,
            'pageName': page,
            'visitTimestamps': timestamps
        }
        table.put_item(Item=item)


def add_event_metrics(email, sessionId, event_metrics_data):
    table = dynamodb.Table('EventMetrics')
    for event_category, events in event_metrics_data.items():
        for event in events:
            item = {
                'email': email,
                'sessionId': sessionId,
                'eventCategory': event_category,
                'actionType': event['actionType'],
                'timestamp': event['timestamp'],
                'additionalData': {k: v for k, v in event.items() if k not in ['actionType', 'timestamp']}
            }
            table.put_item(Item=item)



session_data = {
    "userMetrics": {
        "email": "AbhinavCR@inache.co",
        "userID": 113,
        "loginTimestamp": "Tue, 12 Dec 2023 13:21:24 GMT",
        "logoutType": "normal",
        "logoutTimestamp": "Tue, 12 Dec 2023 14:21:24 GMT",
        "sessionDuration": 60
    },
    "userRoles": [
        {
            "role": "CR",
            "roleID": 70,
            "factoryCode": 15,
            "roleActive": [
                "Tue, 12 Dec 2023 13:21:26 GMT",
                "Tue, 12 Dec 2023 13:25:26 GMT",
                "Tue, 12 Dec 2023 14:21:26 GMT",
                "Tue, 12 Dec 2023 13:42:25 GMT"
            ]
        },
        {
            "role": "CM",
            "roleID": 102,
            "factoryCode": 17,
            "company": 1,
            "roleActive": [
                "Tue, 12 Dec 2023 13:22:21 GMT",
                "Tue, 12 Dec 2023 13:52:23 GMT"
            ]
        },
        {
            "role": "CT",
            "roleID": 103,
            "factoryCode": 17,
            "company": 1,
            "roleActive": [
                "Tue, 12 Dec 2023 13:22:22 GMT"
            ]
        }
    ],
    "pageMetrics": {
        "pagesVisited": [
            "home",
            "awareness",
            "broadcast",
            "analytics",
            "profile",
            "settings"
        ],
        "pageVisitTimestamps": {
            "home": [
                "2023-12-04T08:35:00", 
                "2023-12-04T11:00:00" 
            ],
            "awareness": [
                "2023-12-04T09:45:00"
            ],
            "broadcast": [
                "2023-12-04T13:00:00" 
            ],
            "analytics": [
                "2023-12-04T15:30:00"             
            ],
            "profile": [
                "2023-12-04T16:45:00"         
            ],
            "settings": [
                "2023-12-04T17:30:00"            
            ]
        }
    },
    "eventMetrics": {
        "caseUploadSubmit": [
            {
                "actionType": "In-person Case upload submit",
                "timestamp": "Tue, 12 Dec 2023 13:21:35 GMT"
            },
            {
                "actionType": "Suggestion Box Case upload submit",
                "timestamp": "Tue, 12 Dec 2023 13:21:50 GMT"
            }
        ],
        "caseClick": [
            {
                "actionType": "Case clicked from the dashborad",
                "timestamp": "Tue, 12 Dec 2023 13:21:55 GMT",
                "caseID": 764
            },
            {
                "actionType": "Case clicked from the dashborad",
                "timestamp": "Tue, 12 Dec 2023 13:22:05 GMT",
                "caseID": 761
            }
        ]
    }  
}

# email = session_data['userMetrics']['email']
# sessionId = generate_session_id()

# add_user_metrics(session_data, sessionId)

# add_user_roles(email, sessionId, session_data['userRoles'])

# add_page_metrics(email, sessionId, session_data['pageMetrics'])

# add_event_metrics(email, sessionId, session_data['eventMetrics'])




def get_user_metric(email, sessionId):
    table = dynamodb.Table('UserMetrics')
    response = table.get_item(Key={'email': email, 'sessionId': sessionId})
    return response.get('Item')

# user_metrics = get_user_metric('AbhinavCR@inache.co', 'b5e338c8-3421-4f24-8946-25da4c26053e')


def get_user_roles(email, sessionId):
    table = dynamodb.Table('UserRoles')
    response = table.query(
        IndexName='EmailSessionIndex',
        KeyConditionExpression=Key('email').eq(email) & Key('sessionId').eq(sessionId)
    )
    return response.get('Items')

# user_roles = get_user_roles('AbhinavCR@inache.co', 'b5e338c8-3421-4f24-8946-25da4c26053e')


def get_page_visits(email, sessionId):
    table = dynamodb.Table('PageMetrics')
    response = table.query(
        IndexName='EmailSessionIndex',
        KeyConditionExpression=Key('email').eq(email) & Key('sessionId').eq(sessionId)
    )
    return response.get('Items')

# page_visits = get_page_visits('AbhinavCR@inache.co', 'b5e338c8-3421-4f24-8946-25da4c26053e')


def get_event_metrics(email, sessionId):
    table = dynamodb.Table('EventMetrics')
    response = table.query(
        IndexName='EmailSessionIndex',
        KeyConditionExpression=Key('email').eq(email) & Key('sessionId').eq(sessionId)
    )
    return response.get('Items')

# event_metrics = get_event_metrics('AbhinavCR@inache.co', 'b5e338c8-3421-4f24-8946-25da4c26053e')


def scan_table(table_name):
    table = dynamodb.Table(table_name)
    response = table.scan()
    return response['Items']

# all_data = scan_dynamodb_table('UserRoles')

def delete_table(table_name):
    table = dynamodb.Table(table_name)
    table.delete()
    table.wait_until_not_exists()  


# delete_table('UserMetrics')
# delete_table('UserRoles')
# delete_table('PageMetrics')
# delete_table('EventMetrics')


# print(all_data)


# print("user_metrics", user_metrics)

# print("user_roles", user_roles)

# print("page_visits", page_visits)

# print("event_metrics", event_metrics)



############################################################################################


def calculate_active_users(frequency='D'):
    metrics = scan_table('UserMetrics')
    df = pd.DataFrame(metrics)
    df['loginTimestamp'] = pd.to_datetime(df['loginTimestamp'])
    df.set_index('loginTimestamp', inplace=True)
    active_users = df['email'].resample(frequency).nunique()
    return active_users.mean()



# dau = calculate_active_users('D')
# wau = calculate_active_users('W')
# mau = calculate_active_users('M')

# print(f"DAU: {dau}, WAU: {wau}, MAU: {mau}")

# print("Daily Active Users:", dau)
# print("Weekly Active Users:", wau)
# print("Monthly Active Users:", mau)


def get_average_session_duration(start_date, end_date):
    sessions = scan_table('UserMetrics')

    durations = []
    for session in sessions:
        login_time = parse(session['loginTimestamp'])
        logout_time = parse(session['logoutTimestamp'])
        if start_date <= login_time.date() <= end_date:
            duration = ((logout_time - login_time).total_seconds()) / 60
            durations.append(duration)

    if durations:
        return np.mean(durations)
    else:
        return 0

start_date = datetime(2023, 12, 1).date()
end_date = datetime(2023, 12, 31).date()

# average_duration = get_average_session_duration(start_date, end_date)
# print(f"Average Session Duration: {average_duration} minutes")




def get_average_pages_per_session():
    sessions = scan_table('PageMetrics')

    session_page_counts = defaultdict(int)
    for session in sessions:
        session_id = session['sessionId']
        page_visits = len(session['visitTimestamps'])
        session_page_counts[session_id] += page_visits

    # Calculate average pages per session
    total_pages = sum(session_page_counts.values())
    total_sessions = len(session_page_counts)
    
    if total_sessions > 0:
        average_pages_per_session = total_pages / total_sessions
        return average_pages_per_session
    else:
        return 0

# average_pages = get_average_pages_per_session()
# print(f"Average Pages per Session: {average_pages}")




def calculate_bounce_rate():
    user_sessions = scan_table('UserMetrics')
    page_visits = scan_table('PageMetrics')

    sessions_with_page_visits = set()
    for visit in page_visits:
        if visit['pageName'] != 'home' or len(visit['visitTimestamps']) > 1:
            sessions_with_page_visits.add(visit['sessionId'])

    bounces = 0
    for session in user_sessions:
        session_id = session['sessionId']
        login_time = datetime.strptime(session['loginTimestamp'], "%a, %d %b %Y %H:%M:%S GMT")
        logout_time = datetime.strptime(session['logoutTimestamp'], "%a, %d %b %Y %H:%M:%S GMT")
        session_duration = (logout_time - login_time).total_seconds()

        if (session['sessionId'] not in sessions_with_page_visits and (session['logoutType'] == 'Session Logout' or session_duration <= 60)):
            bounces += 1

    total_sessions = len(user_sessions)
    bounce_rate = (bounces / total_sessions) * 100 if total_sessions > 0 else 0

    return bounce_rate

# bounce_rate = calculate_bounce_rate()
# print(f"Bounce Rate: {bounce_rate}%")



def count_role_logins():
    roles_data = scan_table('UserRoles')

    role_counts = {
        "SUPER_ADMIN": 0,
        "REGIONAL_ADMIN": 0,
        "FACTORY_ADMIN": 0,
        "CR": 0,  # Case Reporter
        "CM": 0,  # Case Manager
        "CT": 0   # Case Troubleshooter
    }

    for role_entry in roles_data:
        role = role_entry['role']
        if role in role_counts:
            role_counts[role] += 1

    return role_counts

# role_logins_count = count_role_logins()
# print("Role Logins Count:", role_logins_count)





def calculate_user_retention(start_date, end_date):
    metrics_data = scan_table('UserMetrics')
    
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

    total_users_at_start = set()
    active_users_throughout = set()


    for entry in metrics_data:
        login_date = datetime.strptime(entry['loginTimestamp'], '%a, %d %b %Y %H:%M:%S GMT')
        if login_date >= start_datetime:
            total_users_at_start.add(entry['email'])
            if login_date <= end_datetime:
                active_users_throughout.add(entry['email'])


    retention_percentage = (len(active_users_throughout) / len(total_users_at_start)) * 100 if total_users_at_start else 0

    return retention_percentage

# retention = calculate_user_retention('2023-12-01', '2023-12-31')
# print(f"User Retention Percentage: {retention}%")




def calculate_churn_rate(start_date, end_date):
    metrics_data = scan_table('UserMetrics')
    
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

    total_users_at_start = set()
    active_users_at_end = set()

    for entry in metrics_data:
        login_date = datetime.strptime(entry['loginTimestamp'], '%a, %d %b %Y %H:%M:%S GMT')
        if login_date <= start_datetime:
            total_users_at_start.add(entry['email'])
        if start_datetime <= login_date <= end_datetime:
            active_users_at_end.add(entry['email'])

    churned_users = total_users_at_start - active_users_at_end
    churn_rate = (len(churned_users) / len(total_users_at_start)) * 100 if total_users_at_start else 0

    return churn_rate

# churn_rate = calculate_churn_rate('2023-12-01', '2023-12-31')
# print(f"Churn Rate: {churn_rate}%")










