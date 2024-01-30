import boto3
from boto3.dynamodb.conditions import Key
import uuid

def get_dynamodb_local():
    return boto3.resource('dynamodb', 
                          region_name='localhost', 
                          endpoint_url='http://localhost:8001', 
                          aws_access_key_id='fakeMyKeyId', 
                          aws_secret_access_key='fakeSecretAccessKey')


dynamodb = get_dynamodb_local() 


def create_user_session_data_table():
    #dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName='UserSessionData',
        KeySchema=[
            {'AttributeName': 'email', 'KeyType': 'HASH'}, 
            {'AttributeName': 'sessionId', 'KeyType': 'RANGE'} 
        ],
        AttributeDefinitions=[
            {'AttributeName': 'email', 'AttributeType': 'S'},
            {'AttributeName': 'sessionId', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

# user_session_data_table = create_user_session_data_table()


def generate_session_id():
    return str(uuid.uuid4())


def add_user_session_data(session_data, session_id):
    table = dynamodb.Table('UserSessionData')
    session_item = {
        'email': session_data['userMetrics']['email'],
        'sessionId': session_id, 
        'loginTimestamp': session_data['userMetrics']['loginTimestamp'],
        'logoutType': session_data['userMetrics']['logoutType'],
        'logoutTimestamp': session_data['userMetrics']['logoutTimestamp'],
        'sessionDuration': session_data['userMetrics']['sessionDuration'],
        'userRoles': session_data['userRoles'],
        'pageVisits': session_data['pageMetrics']['pageVisitTimestamps'],
        'eventMetrics': session_data['eventMetrics']
    }
    response = table.put_item(Item=session_item)

    return response

data = {
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

# add_user_session_data(data, generate_session_id())


def get_user_session_data(email, session_id):
    table = dynamodb.Table('UserSessionData')
    response = table.get_item(Key={'email': email, 'sessionId': session_id})
    return response.get('Item')

# session_data = get_user_session_data('AbhinavCR@inache.co', 'e849364a-d7c0-4012-90f0-4c4d45bb61a6')


def get_user_session_by_email(email):
    table = dynamodb.Table('UserSessionData')
    response = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    return response['Items']

# email = 'AbhinavCR@inache.co'
# items = get_user_session_by_email(email)

def scan_dynamodb_table():
    table = dynamodb.Table('UserSessionData')
    response = table.scan()
    return response['Items']

# all_data = scan_dynamodb_table()

# print(all_data)

# print(items)

# print(session_data)



