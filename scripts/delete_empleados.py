import os
import sys
import django

# Ensure project root is on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_asistencia.settings')
django.setup()

from app.models import Empleado


def norm(s: str) -> str:
    return ' '.join((s or '').strip().lower().split())


def main():
    targets = {"iris", "romulo", "ruben dario", "rubén dario"}
    to_delete_ids = []
    preview = []

    for e in Empleado.objects.all():
        full = norm(f"{e.nombres} {e.apellidos}")
        nombres_n = norm(e.nombres)
        apellidos_n = norm(e.apellidos)

        match = False
        if full in targets:
            match = True
        elif nombres_n in targets or apellidos_n in targets:
            match = True
        else:
            # Manejo flexible para "ruben dario"
            if ("ruben" in nombres_n or "rubén" in nombres_n) and ("dario" in full or "darío" in full):
                match = True

        if match:
            to_delete_ids.append(e.id_empleado)
            preview.append(f"- {e.id_empleado}: {e.nombres} {e.apellidos} (DNI: {e.dni})")

    print("Empleados detectados para eliminar:")
    if not to_delete_ids:
        print("(ninguno)")
        return 0

    print("\n".join(preview))
    deleted_info = Empleado.objects.filter(id_empleado__in=to_delete_ids).delete()
    print("\nEliminación realizada.")
    print(f"Total eliminados (Empleado): {deleted_info[0]}")
    # deleted_info es una tupla (num_total, { 'app.Model': count, ...})
    for model_label, count in deleted_info[1].items():
        print(f"  - {model_label}: {count}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
