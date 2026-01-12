web: python manage.py collectstatic --noinput --settings=taskboard.settings_prod && gunicorn taskboard.wsgi --log-file - --env DJANGO_SETTINGS_MODULE=taskboard.settings_prod
