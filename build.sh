#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.get(username='admin').set_password('admin').save()" | python manage.py shell
echo "from .models import GzzEstadoRegistro; GzzEstadoRegistro.objects.create('A', 'Activo', null)" | python manage.py shell