import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthbodycoach.settings')

# Create a new Celery instance.
app = Celery('BodyHealthCoach')

# Configure Celery using the Django settings.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered apps.
app.autodiscover_tasks()
