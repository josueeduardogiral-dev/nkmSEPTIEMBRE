#!/bin/bash
set -euo pipefail

# Verify the configured server before applying migrations. Never print credentials.
python manage.py verificar_bd --solo-conexion
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Explicit opt-in: only seed the bundled employee list when requested.
if [ "${CARGAR_DATOS_INICIALES:-False}" = "True" ]; then
    python manage.py cargar_empleados
fi
python manage.py verificar_bd

exec gunicorn control_asistencia.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
