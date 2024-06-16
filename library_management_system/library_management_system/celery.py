from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_management_system.settings')

app = Celery('library_management_system')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'send-return-date-exceeded-emails-every-minute': {
        'task': 'library.tasks.send_return_date_exceeded_emails',
        'schedule': crontab(minute='*/1'),   # Schedule to run every minute
    },
}
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))