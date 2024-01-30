# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InacheBackend.settings.dev')
print( os.environ.get('DJANGO_SETTINGS_MODULE'),"DJANGO_SETTINGS_MODULE")


# create a Celery instance and configure it using the settings from Django
celery_app = Celery('InacheBackend')

# Load task modules from all registered Django app configs.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
celery_app.autodiscover_tasks()


celery_app.conf.beat_schedule = {
    'run-notification-engine-every-1-minutes': {
        'task': 'accounts.tasks.run_notification_engine',
        'schedule': crontab(minute='*/1'),
    },
}