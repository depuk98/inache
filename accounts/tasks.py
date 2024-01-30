# your_app/tasks.py
from celery import shared_task
from django.core.management import call_command

@shared_task
def run_notification_engine():
    call_command('notify')
