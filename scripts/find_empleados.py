import os
import sys
import django

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_asistencia.settings')
django.setup()

from app.models import Empleado
from django.db.models import Q

def norm(s: str) -> str:
    return ' '.join((s or '').strip().lower().split())

def main():
    tokens = ['iris', 'rom', 'ruben', 'rubén', 'dario', 'darío']
    qs = Empleado.objects.all()
    print(f"Total empleados: {qs.count()}")

    for t in tokens:
        m = Empleado.objects.filter(Q(nombres__icontains=t) | Q(apellidos__icontains=t))
        print(f"\nCoincidencias para '{t}' ({m.count()}):")
        for e in m:
            print(f"- {e.id_empleado}: {e.nombres} {e.apellidos} (DNI: {e.dni})")

if __name__ == '__main__':
    main()
