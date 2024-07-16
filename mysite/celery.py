# # beat_schedule.py

# from celery.schedules import crontab
# from celery_app import app
# from celery import Celery

# app = Celery('tasks')

# app.conf.beat_schedule = {
#     'run-processing-task-every-night': {
#         'task': 'tasks.run_processing_task',
#         'schedule': crontab(minute=0, hour=0),  # Run at midnight
#     },
# }

# app.conf.timezone = 'UTC'

# mysite/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'scrape-and-process-schemes-every-5-minutes': {
        'task': 'myapp.tasks.scrape_and_process_schemes',
        'schedule': crontab(minute='*/5'),  
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

