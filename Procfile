web: python manage.py migrate && python manage.py collectstatic && gunicorn --workers 4 --worker-class eventlet --timeout 180 healthbodycoach.wsgi
