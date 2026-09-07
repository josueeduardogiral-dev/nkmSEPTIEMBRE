# fix_admin.py
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_asistencia.settings')
django.setup()

from django.contrib.auth import get_user_model

U = get_user_model()
user = U.objects.filter(username='admin').first()

if user:
    user.set_password('Nakama@2025')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print('OK Usuario admin actualizado')
else:
    user = U.objects.create_superuser('admin', 'admin@nakama.com', 'Nakama@2025')
    print('OK Usuario admin creado')

print(f'Usuario: admin')
print(f'Contraseña: Nakama@2025')
print(f'is_staff: {user.is_staff}')
print(f'is_superuser: {user.is_superuser}')
