#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
# echo "from django.contrib.auth.models import User; list(User.objects.filter(is_superuser=True).values_list('admin', flat=True))" | python manage.py shell
echo "from .models import GzzEstadoRegistro; GzzEstadoRegistro.objects.create('A', 'Activo', null)" | python manage.py shell