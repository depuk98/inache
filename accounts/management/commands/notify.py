import csv
import json
import time
import traceback
from django.apps import apps
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import FieldDoesNotExist
from dateutil.relativedelta import relativedelta
import pytz
from django.core.exceptions import FieldError, ObjectDoesNotExist
from accounts.Service.CasesService import dueDate
from accounts.Utils.NotificationUtil.CaseCondtions import ConditionMappings
from django.core.management.base import BaseCommand
import accounts.Utils.NotificationUtil.FunctionMapping
from accounts.Utils.NotificationUtil.FunctionMapping import FUNCTION_MAPPINGS
from accounts.Utils.NotificationUtil.collated_cases_csv import cases_csv
from accounts.Utils.NotificationUtil.variables import VariablesMapping
from accounts.classes.AwsUtil import AwsUtil
from accounts.constants import CaseActiveStatus, CaseStatus
from accounts.models import Case, Notification,NotificationLog, UserRoleFactory, BaseUserModel
from InacheBackend.settings.base import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SES_REGION_NAME
from accounts.models import Notification
from accounts.serializers import PasswordResetLinkGenerator
import boto3
import logging
from django.core.signing import Signer
from datetime import date
from django.core.mail import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
from django.template.loader import render_to_string

class RuleParser:
    def __init__(self, rule_definition):
        # Directly assign the dictionary, no need for json.loads()
        self.rule_definition = rule_definition
        self.step_results = {}
        logging.info(f"Initialized RuleParser with rule_definition: {self.rule_definition}")

    def execute(self):
        print("Executing rule...")
        for step in self.rule_definition["steps"]:
            try:
                print(step)
                self.execute_step(step)
            except Exception as e:
                logging.info(f"Error executing step: {e}")
        print(f"Final result: {self.step_results.get('final_result')}")
        # Process the 'then' section after all steps and conditions have been executed
        action = self.rule_definition.get('then', {})
        result = None  # Initialize result

        time_threshold = self.rule_definition.get('conditions', {}).get('check_last_login', {}).get("time_threshold_minutes", {})

        if 'send_email_to' in action:
            result = self.handle_send_email_to(action['send_email_to'], time_threshold)
        
        # Add more actions here as needed, e.g., if 'some_other_action' in action: ...
        return result  # Return the result
    def handle_send_email_to(self, send_email_to_action, time_threshold):
        notification_data = []
        final_queryset = self.step_results.get("final_result")
        
        print("final_queryset", final_queryset)
        
        now = timezone.now()
        # Determine the source of the user_role_id
        is_direct_role_id = send_email_to_action.get("is_direct_role_id", False)
        field = send_email_to_action.get("field")

        # Handle direct role_id scenario
        if is_direct_role_id:
            if final_queryset:
                for user_role in final_queryset:
                    if user_role.last_login_role is None or time_threshold == {} or (time_threshold and user_role.last_login_role < now - timedelta(minutes=time_threshold)):
                        try:

                            # Initialize case_csv as None
                            case_csv = None

                            # Check if final_queryset is a dictionary and handle accordingly
                            if isinstance(final_queryset, dict):
                                case_csv = final_queryset[user_role]['cases'] if user_role in final_queryset and 'cases' in final_queryset[user_role] else None
                            
                            # If final_queryset is not a dictionary, it's a QuerySet. Fetch or compute the 'cases' data for the current user_role.
                            # This part of the code should contain the logic to handle the case when final_queryset is a QuerySet.
                            # For example:
                            # if not isinstance(final_queryset, dict):
                            #     cases_data = user_role.cases.all()  # Adjust based on your actual data model.
                            # Assuming user_role is an instance of UserRoleFactory
                            print(type (final_queryset))
                            base_user = user_role.user_fk
                            notification_obj = {
                                'user_id': base_user.id,
                                'role_id': user_role.id,
                                'role': user_role.role.role,
                                'email': base_user.email,
                                'phone_number': base_user.mobile_number,
                                'factory_fk': user_role.factory_fk.id if user_role.factory_fk else None,
                                'region_fk': user_role.region_fk if user_role.region_fk else None,
                                'case_csv':case_csv,
                            }
                            notification_data.append(notification_obj)
                            print("notification_obj", notification_obj)
                        except UserRoleFactory.DoesNotExist:
                            logging.info(f"UserRoleFactory with ID {field} does not exist.")
                        except BaseUserModel.DoesNotExist:
                            logging.info(f"BaseUserModel associated with UserRoleFactory ID {field} does not exist.")
                    else:
                        pass
            else:
                logging.info("No matching records found in the final result.")

        # Handle the scenario where you need to extract the role_id from a related case
        elif isinstance(final_queryset, (dict)) and is_direct_role_id == False:
            cr=final_queryset['cr']
            cm=final_queryset['cm']
            ct=final_queryset['ct']
            notification_data=[]
            print(final_queryset,"fsdfdsfdnjferif ej fei i")
            for cruser in cr:
                notification_obj={'userRole':cruser,
                                    'user_name':cruser.user_fk.user_name,
                                    'email':cruser.user_fk.email,
                                    'role':cruser.role.role,
                                    'collated_link_to_cases':cr[cruser]
                                    }
                notification_data.append(notification_obj)
            for cmuser in cm:
                notification_obj={'userRole':cmuser,
                                    'user_name':cmuser.user_fk.user_name,
                                    'email':cmuser.user_fk.email,
                                    'role':cmuser.role.role,
                                    'collated_link_to_cases':cm[cmuser]
                }
                notification_data.append(notification_obj)
            for ctuser in ct:
                notification_obj={'userRole':ctuser,
                                    'user_name':ctuser.user_fk.user_name,
                                    'email':ctuser.user_fk.email,
                                    'role':ctuser.role.role,
                                    'collated_link_to_cases':ct[ctuser]
                }
                notification_data.append(notification_obj)
                
        else:
            print("final_queryset2", final_queryset)
            if final_queryset is not None:
                
                for case in final_queryset:
                    print("Case", case)
                    user_role_id = getattr(case, field, None)
                    print(user_role_id)
                    if user_role_id:
                        user_role = UserRoleFactory.objects.get(id=user_role_id)
                        print("print(vars(case))",vars(case))
                        print(time_threshold) 
                        if user_role.last_login_role is None or time_threshold == {} or (time_threshold and user_role.last_login_role < now - timedelta(minutes=time_threshold)):
                            try:
                                base_user = user_role.user_fk
                                notification_obj = {
                                    'case_id': case.id,
                                    'case_number': case.CaseNumber,
                                    'user_id': base_user.id,
                                    'role_id': user_role.id,
                                    'role': user_role.role.role,
                                    'email': base_user.email,
                                    'phone_number': base_user.mobile_number,
                                    'factory_fk': user_role.factory_fk.id if user_role.factory_fk else None,
                                    'region_fk': user_role.region_fk if user_role.region_fk else None,
                                    
                                } 
                                notification_data.append(notification_obj)
                                print("notitification_obj",notification_obj )
                            except UserRoleFactory.DoesNotExist:
                                logging.info(f"UserRoleFactory with ID {user_role_id} does not exist.")
                            except BaseUserModel.DoesNotExist:
                                logging.info(f"BaseUserModel associated with UserRoleFactory ID {user_role_id} does not exist.")
                        else:
                            pass
       
                        
                        
            else:
                logging.info("No matching records found for the final result.")
        print(f"Notification data: {notification_data}")
        return notification_data

    def execute_step(self, step):
        try:
            model = apps.get_model('accounts', step["model"])
        except LookupError as e:
            raise ValueError(f"Error retrieving model: {e}")

        queryset = model.objects.all()
        print(queryset)
        logging.info(f"Executing step for model: {model.__name__}")

        for condition_key in step.get("conditions", []):
            print(f"Applying condition: {condition_key}")
            if condition_key in ConditionMappings.CONDITIONS:
                condition_model, condition_query = ConditionMappings.CONDITIONS[condition_key]
                if model != condition_model:
                    raise ValueError(f"Condition {condition_key} not valid for model {step['model']}")
                try:
                
                    queryset = queryset.filter(condition_query)
                    print("utut",queryset)
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                print("queryset",queryset)

        for action in step.get("actions", []):
            print(f"Performing action: {action}")
            try:
                
                if action["type"] == "fetch_ids":
                    fetched_ids = list(queryset.values_list('id', flat=True))
                    self.step_results[action["store_as"]] = fetched_ids
                    logging.info(f"Fetched IDs: {fetched_ids}")
                elif action["type"] == "filter":
                    filter_on = action.get("filter_on")
                    filter_values = self.step_results.get(action.get("filter_values"), [])
                    store_as = action.get("store_as", "default_queryset")
                    # Check if filter_on is a valid field in the model
                    try:
                        model._meta.get_field(filter_on)
                    except FieldDoesNotExist:
                        raise ValueError(f"The field '{filter_on}' does not exist in model '{model.__name__}'.")

                    # Check if filter_values contains filter_on variable
                    if not filter_values:
                        raise ValueError(f"No filter values provided for field '{filter_on}'.")

                    # Apply filter
                    try:
                        if(store_as):
                            queryset = queryset.filter(**{filter_on + "__in": filter_values})
                            self.step_results[store_as] = queryset
                        else:
                            self.step_results["final_result"] = queryset
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
                    print(f"Filtered queryset based on: {filter_on} and now the queryset is {queryset}" )
                
                elif action["type"] == "combine_querysets":
                    queryset1_key = action.get("queryset1")
                    queryset2_key = action.get("queryset2")
                    store_as = action.get("store_as", "combined_queryset")

                    # Retrieve the querysets from step_results
                    queryset1 = self.step_results.get(queryset1_key)
                    queryset2 = self.step_results.get(queryset2_key)
                    print("queryset2222",queryset2)
                    print("queryset111",queryset1)
                    # Check if both querysets exist and are from the same model
                    if queryset1 is not None and queryset2 is not None and queryset1.model == queryset2.model:
                        combined_queryset = queryset1.union(queryset2)
                        self.step_results[store_as] = combined_queryset
                        print(f"Combined querysets stored as '{store_as}'.")
                        print("combined_queryset",combined_queryset)
                        
                    else:
                        raise ValueError("Querysets to combine are missing or from different models.")
                    
                elif action["type"] == "fetch_results":
                    result_in = action.get("result_in")
                    if result_in and result_in in self.step_results:
                        self.step_results["final_result"] = self.step_results[result_in]
                    else:
                        self.step_results["final_result"] = queryset
                    print("Stored final result:", self.step_results["final_result"])
                elif action["type"] == "fetch_queryset":
                    store_as = action.get("store_as", "default_queryset")
                    self.step_results[store_as] = queryset
                    print(f"Stored queryset as '{store_as}'.")
                elif action["type"] == "fetch_field_values":
                    field_name = action["field_name"]
                    fetched_field_values = list(queryset.values_list(field_name, flat=True))
                    self.step_results[action["store_as"]] = fetched_field_values
                    print(f"Fetched {field_name} values: {fetched_field_values} count: {len(fetched_field_values)}")
                elif action["type"] == "call_function":
                    print("here function ")
                    self.handle_call_function(action, queryset)
            except FieldError as e:
                raise ValueError(f"Invalid field in action '{action['type']}': {e}")
            except KeyError as e:
                raise ValueError(f"Missing key in action '{action['type']}': {e}")
    
    def handle_call_function(self, action, queryset):
        function_name = action.get("function")
        store_as = action.get("store_as")
        raw_params = action.get("params", {})  # Dictionary of parameters
        # Process parameters to fetch values from step_results if needed
        params = {}
        for param, value in raw_params.items():
            if isinstance(value, str) and value.startswith("result:"):
                # Fetch from step_results
                result_key = value.split(":", 1)[1].strip()
                print("diplo",result_key)
                params[param] = self.step_results.get(result_key)
            else:
                # Use the value as is
                params[param] = value
        print(params)
        # Call the function with processed parameters
        if function_name in FUNCTION_MAPPINGS:
            func = FUNCTION_MAPPINGS[function_name]
            print("Function to call:", func)
            print("Parameters to pass:", params)
            func_params = {k: v for k, v in params.items() if k != 'queryset'}
            try:
                # Pass the queryset separately
                result_queryset = func(queryset, **func_params)
                print("triresult_queryset",(result_queryset))
            except Exception as e:
                raise ValueError(f"Error during function execution: {e}")
            self.step_results[store_as] = result_queryset
        else:
            raise ValueError(f"Function {function_name} is not defined.")

def VariableMapping(vars,data):
    for var in vars:
        value=""
        csv = [[]]
        if var in data.keys():
            print(var,data[var])
            value=data[var]
        elif var in VariablesMapping.VARIABLES:  
            query_info=VariablesMapping.VARIABLES[var]
            model = query_info["model"]
            field = query_info["field"]
            id_field = query_info["id_field"]
            key=query_info["key"]
            value = model.objects.values_list(field, flat=True).get(**{id_field: data[key]})
            if var == "role_id":
                print("role_in_after vriable mapping ", value)
            if(isinstance(value,datetime)==True):
                logging.info("Checking if it's coming inside the if condition")
                value = value.strftime("%Y-%m-%d %H:%M:%S %Z")
            print("vars[var]",vars[var])
        elif var == "sla_due_date_and_time":
                user=UserRoleFactory.objects.get(id=data["role_id"])
                unsorted_new_cases_response_body = None
                unsorted_new_cases_response_body = list(Case.objects.filter(id=data["case_id"]).values(
                    "id",
                    "CaseNumber",
                    "ReportingMedium",
                    "Date",
                    "CurrentStatus",
                    "Complainer__Registered",
                    "reopened"
                ))
                new_cases_response_body= sorted(unsorted_new_cases_response_body, key=lambda x: x['Date'], reverse=True)
                duedatteee = dueDate(new_cases_response_body, user.role.role)  
                value = duedatteee[0]["dueDate"]
                if(isinstance(value,datetime)==True):
                    value = value.strftime("%Y-%m-%d %H:%M:%S %Z")
                    print("dueDate format",duedatteee[0]["dueDate"] )
        elif var == "role":
            value = data["role"]
        elif var == "role_id":
            value = data["role_id"]
        elif var == "user_id":
            value = data["user_id"]  
        elif var == "xlxs":
            csv = data["case_csv"]
            print(data,"dasdsadefefewkfnkwefncewl ")
        elif var == "month":
            value == datetime.now().month
        elif var == "week":
            year, week_num, day_of_week = datetime.now().isocalendar()
            value = week_num
        elif var == "date_today":
            value = str(date.today())
            print(value)
        elif var == "password_reset_link": 
            user=BaseUserModel.objects.get(id=data["user_id"])
            url = PasswordResetLinkGenerator.generate(user )
            print(url)
            value = url
        if csv != [[]]: 
            vars[var] = csv
        else:    
            vars[var] = value
    return vars



class Command(BaseCommand):
    help = 'Run the notification engine'

    def handle(self, *args, **options):
        print("Starting notification engine")
        # coallatecasescrcmct()
        count =0
        try:
            notifications = Notification.objects.all()
            logging.info(f"Found {len(notifications)} notifications")
            for notification in notifications:
                if notification.is_active:
                    # Check the schedule before processing the rules
                    # Parse the notification rules JSON string into a dictionary
                    try:
                        notification_rules = notification.notification_rules
                    except json.JSONDecodeError as e:
                        logging.info(f"Failed to parse notification rules: {e}")
                        continue  # Skip to the next notification if parsing fails

                    # If the notification hasn't been sent, proceed with rule parsing
                    try:
                        rule_parser = RuleParser(notification_rules)
                        notification_data = rule_parser.execute()
                        print(type(notification_data),"ffbhewibfiwebfiwebfweifbiwe")
                        if notification_data:
                            for data in notification_data:
                                event_identifier = {}
                                items = notification.event_identifier_items  # Assuming this is a JSON string
                                event_identifier = VariableMapping(items,data)
                                print("qweqweqwewqe",event_identifier)
                                if notification.schedule and notification.event_identifier_items:
                                    print("here", notification.schedule, notification.event_identifier_items)
                                    schedule_parser = ScheduleParser(notification.schedule)
                                    event_identifier = notification.event_identifier_items or None
                                    
                                    if schedule_parser.was_notification_sent(notification.id, event_identifier):
                                        print("heree")
                                        print(f"Notification already sent for {notification.subscription_to_be_triggered}")
                                        continue  # Skip to the next notification
                                    # Get the email you're about to send to
                                    email_to_send = data.get('email')
                                    # Query the NotificationLog to find if a log exists with the same event_identifier
                                    existing_logs = NotificationLog.objects.filter(
                                        notification_fk=notification.id,
                                        event_identifier=event_identifier  # Checking if the event_identifier matches
                                    )
                                    # Initialize a flag to determine if the notification was already sent
                                    already_sent = False
                                    # Now, iterate over the existing logs to check if any match the 'send_to' email
                                    for log_entry in existing_logs:
                                        try:
                                            # Parse the log field, which is expected to contain JSON
                                            log_data = log_entry.log
                                            # Use the .get method to safely access the 'send_to' key
                                            send_to_emails = log_data.get("send_to")
                                            # Check if the email_to_send is in the list of 'send_to' emails
                                            if send_to_emails and email_to_send in send_to_emails:
                                                already_sent = True
                                                break
                                        except json.JSONDecodeError:
                                            # Handle the case where the log entry isn't valid JSON
                                            logging.info(f"Invalid JSON in log entry: {log_entry.id}")
                                    # If the notification was already sent, skip sending it again
                                    if already_sent:
                                        print(f"Notification already sent to {email_to_send} for {event_identifier}")
                                        continue  # Skip sending the notification again
                                print(type(data),"dasfsfjkewdfkjwde fj wdj fkwj")
                                email = data.get('email')
                                case_number = data.get('case_number')
                                print(data,"identifoer")
                                body=notification.template_fk.body
                                subject=notification.template_fk.subject
                                vars=notification.template_fk.variables
                                print("gyyegye", data)
                                vars=VariableMapping(vars,data)
                                print(vars,"dnjiadnjiadnjnnwejndjnwidjwnij")
                                formatted_email = body.format(**vars)
                                subject=subject.format(**vars)
                                user=BaseUserModel.objects.get(email=email)
                                signer = Signer()
                                token = signer.sign(str(user.id))
                                if "xlsx" in notification.template_fk.title:
                                    cases_csv(data,email,notification,formatted_email)
                                    continue
                                # collated_csv_data={'headers':fieldnames,'data':convert_to_json_serializable(data['case_csv'])}
                                #vars=json.loads(notification.template_fk.variables) // sometimes works and sometime doesn't
                               
                                # if vars["xlxs"]:
                                #     with open("cases.csv", 'rb') as file:
                                #         formatted_email.attach(filename="cases.csv", content=file.read(), mimetype='text/csv')
                                print("formatted_email",formatted_email)
                                print("event_identifier", event_identifier)
                                print(f'Sending notification to {email} for case {case_number}')
                                

                                message_data = {
                                        'eventType': 'userNotification',
                                        'emailList': [email],
                                        'subject': subject,
                                        'message': formatted_email,
                                        'notification': notification.id,
                                        'event_identifier': (event_identifier),
                                        
                                    }
                                
                                TopicArn='arn:aws:sns:ap-south-1:300380748892:Test_Topic'
                                aws= AwsUtil(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SES_REGION_NAME)
                                # time.sleep(2)
                                response=aws.publish_message_to_sns(TopicArn,message_data)
                                count = count +1
                                logging.info(response, count)
                                logging.info(len(notification_data))
                        else:
                            logging.info(f'No notification for {notification.subscription_to_be_triggered}')
                    except Exception as e:
                        logging.info(f"Error processing notification: {e}")
                        traceback.print_exc()
                else:
                    logging.info(f"No rules defined for {notification.subscription_to_be_triggered}")
            logging.info(count)       
        except Exception as e:
            logging.info(f"Error retrieving notifications: {e}")
            traceback.print_exc()
def convert_to_json_serializable(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    else:
        return obj
class ScheduleParser:
    def __init__(self, schedule):
        self.schedule = schedule

    def was_notification_sent(self, notification_id, event_identifier):
        last_sent = NotificationLog.objects.filter(notification_fk=notification_id).order_by('-timestamp').first()
        
        now = datetime.now(pytz.utc)
        time_since_last_sent = timezone.now()
        if last_sent:
            time_since_last_sent = now - last_sent.timestamp

        if self.schedule == "Weekly":
            if NotificationLog.objects.filter(notification_fk =notification_id, event_identifier=event_identifier ):
                if time_since_last_sent < timedelta(days=7):
                    return time_since_last_sent < timedelta(days=7)
            else:
                return False
        elif self.schedule == "Monthly":
            if NotificationLog.objects.filter(notification_fk =notification_id, event_identifier=event_identifier ):
                if time_since_last_sent < timedelta(days=30):
                    return time_since_last_sent < timedelta(days=30)
            else:
                return False
        elif self.schedule == "Daily":
            if NotificationLog.objects.filter(notification_fk =notification_id, event_identifier=event_identifier ):
                if time_since_last_sent < timedelta(days=1):
                    return time_since_last_sent < timedelta(days=1)
            else:
                return False
        elif self.schedule == "Once_in_2Days":
            if NotificationLog.objects.filter(notification_fk =notification_id, event_identifier=event_identifier ):
                if time_since_last_sent < timedelta(days=2):
                    return time_since_last_sent < timedelta(days=2)
            else:
                return False        
        elif self.schedule == "Every_3rd_6th_day":
            print("case_assgined_to_CT_datetimehuhuhu",event_identifier["case_assgined_to_CT_datetime"])
            # Assuming event_identifier.case_assgined_to_CT_datetime is a datetime of when the case was assigned
            case_assigned_to_CT = event_identifier["case_assgined_to_CT_datetime"]
            # Check if case_assigned_to_CT is a string, and convert it to datetime if it is
            if isinstance(case_assigned_to_CT, str):
                # Adjust the format string as per your actual datetime format
                case_assigned_to_CT = datetime.strptime(case_assigned_to_CT, '%Y-%m-%d %H:%M:%S %Z').replace(tzinfo=pytz.utc)
            # Ensure case_assigned_to_CT is timezone-aware
            if case_assigned_to_CT.tzinfo is None or case_assigned_to_CT.tzinfo.utcoffset(case_assigned_to_CT) is None:
                case_assigned_to_CT = pytz.utc.localize(case_assigned_to_CT)
            
            # Now both now and case_assigned_to_CT are timezone-aware datetimes
            now = datetime.now(pytz.utc)
            days_since_assignment = (now - case_assigned_to_CT).days
            is_third_or_sixth_day = days_since_assignment in [2, 5] 

            # 0-indexed: 2 for the 3rd day, 5 for the 6th day
            # Check if it's the 3rd or 6th day since the case was assigned
            if is_third_or_sixth_day:
                print("is_third_or_sixth_day",is_third_or_sixth_day,now.date())
                # Check if a notification has already been sent today
                if NotificationLog.objects.filter(
                        notification_fk=notification_id,
                        event_identifier=event_identifier,
                        timestamp__date=now.date()
                ).exists():
                    return True  # No notification sent today, so we should send one
                else:
                    return False
            else:
                return True
            
        elif self.schedule == "Every_2nd_3rd_day":
            case_assigned_to_CT = event_identifier["case_assgined_to_CT_datetime"]
            if isinstance(case_assigned_to_CT, str):
                case_assigned_to_CT = datetime.strptime(case_assigned_to_CT, '%Y-%m-%d %H:%M:%S %Z').replace(tzinfo=pytz.utc)
            if case_assigned_to_CT.tzinfo is None or case_assigned_to_CT.tzinfo.utcoffset(case_assigned_to_CT) is None:
                case_assigned_to_CT = pytz.utc.localize(case_assigned_to_CT)
            now = datetime.now(pytz.utc)
            days_since_assignment = (now - case_assigned_to_CT).days
            is_second_or_third_day = days_since_assignment in [1, 2] 
            if is_second_or_third_day:
                if NotificationLog.objects.filter(
                        notification_fk=notification_id,
                        event_identifier=event_identifier,
                        timestamp__date=now.date()
                ).exists():
                    return True
                else:
                    return False
            else:
                return True
                
        elif self.schedule == "Every_7_15_25_29_thday":
            case_assigned_to_CT = event_identifier["case_assgined_to_CT_datetime"]
            if isinstance(case_assigned_to_CT, str):
                case_assigned_to_CT = datetime.strptime(case_assigned_to_CT, '%Y-%m-%d %H:%M:%S %Z').replace(tzinfo=pytz.utc)
            if case_assigned_to_CT.tzinfo is None or case_assigned_to_CT.tzinfo.utcoffset(case_assigned_to_CT) is None:
                case_assigned_to_CT = pytz.utc.localize(case_assigned_to_CT)
            now = datetime.now(pytz.utc)
            days_since_assignment = (now - case_assigned_to_CT).days
            is_7_15_25_29_thday = days_since_assignment in [6,14,24,28]
            if is_7_15_25_29_thday:
                if NotificationLog.objects.filter(
                        notification_fk=notification_id,
                        event_identifier=event_identifier,
                        timestamp__date=now.date()
                ).exists():
                    return True
                else:
                    return False
            else:
                return True
            
        elif self.schedule == "Every_6hrs_After_First":
            case_assigned_to_CM = event_identifier["case_assgined_to_CM_datetime"]
            if isinstance(case_assigned_to_CM, str):
                case_assigned_to_CM = datetime.strptime(case_assigned_to_CM, '%Y-%m-%d %H:%M:%S %Z').replace(tzinfo=pytz.utc)
            if case_assigned_to_CM.tzinfo is None or case_assigned_to_CM.tzinfo.utcoffset(case_assigned_to_CM) is None:
                case_assigned_to_CM = pytz.utc.localize(case_assigned_to_CM)
            now = datetime.now(pytz.utc)
            
            # Calculate the time since the case was assigned in hours
            hours_since_assignment = (now - case_assigned_to_CM).total_seconds() / 3600.0
            is_after_first_6_hours = hours_since_assignment > 6
            is_6_hour_multiple = int(hours_since_assignment) % 6 == 0
            
            # Check if the time since assignment is after the first 6 hours and a multiple of 6 hours
            if is_after_first_6_hours and is_6_hour_multiple:
                if NotificationLog.objects.filter(
                        notification_fk=notification_id,
                        event_identifier=event_identifier,
                        timestamp__date=now.date(),
                        timestamp__hour=now.hour
                ).exists():
                    return True  # Notification already sent in this 6-hour period
                else:
                    return False  # No notification sent in this 6-hour period, should send one
            else:
                return True  # It's either the first 6 hours or not a 6-hour multiple, don't send a notification

        elif self.schedule == "Every_6hrs":
            # If a notification has been sent before
            if last_sent:
                # Calculate the time since the last notification was sent
                time_since_last_sent = now - last_sent.timestamp

                # Check if it's been 6 hours or more since the last notification
                if time_since_last_sent >= timedelta(hours=6):
                    # It's been 6 hours or more, so a new notification should be sent
                    return False
                else:
                    # It's been less than 6 hours since the last notification
                    return True
            else:
                # No notification has been sent before, so send one now
                return False
        elif self.schedule == "Every_24hours_for_3_days":
            logs = NotificationLog.objects.filter(notification_fk=notification_id, event_identifier=event_identifier).order_by('-timestamp')

            # If no logs exist, this is the first notification, so it should be sent.
            if not logs.exists():
                return False  # Indicates a notification should be sent

            # Fetch the first and the latest log
            first_log = logs.last()
            latest_log = logs.first()

            # Calculate the time since the first and the last log were created
            time_since_first_log = now - first_log.timestamp
            time_since_last_log = now - latest_log.timestamp

            # Check if the total duration since the first log is within 3 days
            if time_since_first_log <= timedelta(days=3):
                # Check if at least 24 hours have passed since the last log
                if time_since_last_log >= timedelta(hours=24):
                    return False  # Indicates a notification should be sent
                else:
                    # Less than 24 hours have passed since the last notification
                    return True  # Indicates a notification was recently sent
            else:
                # More than 3 days have passed since the first notification
                return True  # Indicates no more notifications should be sent
            
        elif self.schedule == "Immediate":
            logging.info("event_identifier",event_identifier)
            # Check if an immediate notification has already been sent for the specific event
            if event_identifier:
                return NotificationLog.objects.filter(
                    notification_fk=notification_id, 
                    event_identifier=event_identifier
                ).exists()
            return False
        return False



def send_logs_to_cloudwatch(log_group_name, log_stream_name, logs):
    # Create a CloudWatchLogs client
    
    aws_access_key_id = AWS_ACCESS_KEY_ID
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    aws_region = AWS_SES_REGION_NAME

    cloudwatch_logs = boto3.client(
        'logs',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    # Create or get the log group
    try:
        cloudwatch_logs.create_log_group(logGroupName=log_group_name)
    except cloudwatch_logs.exceptions.ResourceAlreadyExistsException:
        pass  # Log group already exists

    # Create or get the log stream
    try:
        cloudwatch_logs.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    except cloudwatch_logs.exceptions.ResourceAlreadyExistsException:
        pass  # Log stream already exists

    # Put log events
    try:
        cloudwatch_logs.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=logs
        )
    except Exception as e:
        logging.info(f"Failed to send logs to CloudWatch: {e}")