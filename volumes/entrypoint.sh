#!/usr/bin/env bash
set -e

python /srv/webchat/manage.py migrate --noinput

python /srv/webchat/manage.py collectstatic --noinput

ls /srv/webchat/static/
ls /srv/webchat/static/custom/

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'nimba') if User.objects.filter(email='admin@example.com').count() == 0 else User.objects.filter()" | python /srv/webchat/manage.py shell

exec "$@"
