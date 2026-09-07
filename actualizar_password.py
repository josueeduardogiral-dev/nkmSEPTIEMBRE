#!/usr/bin/env python
"""
Script para actualizar la contraseña del usuario especificado.
Ejecutar con: python actualizar_password.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_asistencia.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = 'NakamaSac'
NEW_PASSWORD = 'Nakama!2025'

try:
    u = User.objects.get(username=USERNAME)
    u.set_password(NEW_PASSWORD)
    u.save()
    print(f'✓ Contraseña actualizada correctamente para el usuario: {USERNAME}')
except User.DoesNotExist:
    print(f'✗ Error: El usuario {USERNAME} no existe')
except Exception as e:
    print(f'✗ Error: {e}')
