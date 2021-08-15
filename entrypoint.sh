#!/bin/bash -c
python manage.py migrate
python manage.py loaddata demo_db.json
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@local.domain', 'admin')" | python manage.py shell
python manage.py collectstatic --no-input
exec "$@"