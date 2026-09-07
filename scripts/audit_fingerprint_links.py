import os
import sys
import django

# Ensure project root in path
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_asistencia.settings')
django.setup()

from app.models import DispositivoEmpleado


def main():
    print("Vínculos de dispositivos (fingerprint -> empleado):")
    qs = DispositivoEmpleado.objects.select_related('empleado').all().order_by('creado_en')
    if not qs.exists():
        print("(sin vínculos)")
        return 0
    for v in qs:
        emp = v.empleado
        print(f"- {v.fingerprint} -> {emp.id_empleado} | {emp.apellidos}, {emp.nombres} (DNI {emp.dni}) | {v.creado_en:%Y-%m-%d %H:%M}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
