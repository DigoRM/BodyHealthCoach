web: python manage.py migrate && python manage.py collectstatic && gunicorn --workers 8 --worker-class eventlet --timeout 180 healthbodycoach.wsgi
