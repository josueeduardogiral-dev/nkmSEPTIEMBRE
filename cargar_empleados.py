# cargar_empleados.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_asistencia.settings')
django.setup()

from app.models import Empleado, TipoAsistencia

# Crear empleados (ordenados alfabéticamente por apellidos y luego nombres)
empleados_data = [
    {"nombres": "Claudia", "apellidos": "Aguilar"},
    {"nombres": "Ademir", "apellidos": "Arredondo"},
    {"nombres": "Jonathan Oswaldo", "apellidos": "Azaña Ramos"},
    {"nombres": "Jose Angel", "apellidos": "Borda Hernandez"},
    {"nombres": "Valery", "apellidos": "Celestino Begar"},
    {"nombres": "Edwin", "apellidos": "Chaparro Ampa"},
    {"nombres": "Jose Alberto", "apellidos": "Davila Paredes"},
    {"nombres": "Jean Leonardo", "apellidos": "Estrada Roque"},
    {"nombres": "Marco Antonio Jose", "apellidos": "Garcia Galvan"},
    {"nombres": "Thalia", "apellidos": "Giral Onton"},
    {"nombres": "Jose Luis", "apellidos": "Gonzalez Romero"},
    {"nombres": "Pedro Luis", "apellidos": "Hernandez Reyes"},
    {"nombres": "Edson Pavel", "apellidos": "Ipenza"},
    {"nombres": "Joel Edwin", "apellidos": "Llanos Mejico"},
    {"nombres": "Carlos Fernando", "apellidos": "Lozano Roman"},
    {"nombres": "Carlos Gabriel", "apellidos": "More Miranda"},
    {"nombres": "Willy Jhon", "apellidos": "Paco Deza"},
    {"nombres": "David Eduardo", "apellidos": "Pauta Juarez"},
    {"nombres": "Julio Daniel", "apellidos": "Peñaherrera Orrillo"},
    {"nombres": "Jordi Cesar Hernando", "apellidos": "Quezada Rosales"},
    {"nombres": "Wilmer", "apellidos": "Quispe Huaringa"},
    {"nombres": "Cecy Kattia", "apellidos": "Salcedo Arauda"},
    {"nombres": "Jose Lino", "apellidos": "Solano Caqui"},
    {"nombres": "Jaime Franksue", "apellidos": "Sullon Li"},
    {"nombres": "Yuli", "apellidos": "Tarazona"},
    {"nombres": "Alexis", "apellidos": "Vasquez Conchatupac"},
    {"nombres": "Zhihua Santiago", "apellidos": "Yong Sanchez"}
]

empleados_data_sorted = sorted(
    empleados_data,
    key=lambda e: (e["apellidos"].lower(), e["nombres"].lower())
)

# Crear empleados
for emp_data in empleados_data_sorted:
    Empleado.objects.get_or_create(
        nombres=emp_data["nombres"],
        apellidos=emp_data["apellidos"]
    )

# Crear tipos de asistencia si no existen
tipos = [
    'Entrada', 'Salida', 'Inicio Almuerzo', 'Fin Almuerzo',
    'Entrada por comisión', 'Salida por comisión',
    'Entrada por otros', 'Salida por otros'
]
for nombre in tipos:
    TipoAsistencia.objects.get_or_create(nombre_asistencia=nombre)

print("Datos insertados correctamente.")
