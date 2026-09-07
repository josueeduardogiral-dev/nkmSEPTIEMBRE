"""
Carga empleados y tipos de asistencia iniciales.
Uso: python manage.py cargar_empleados
En producción: configurar DATABASE_URL y ejecutar este comando (p. ej. en Railway Run Command).
"""
from django.core.management.base import BaseCommand
from app.models import Empleado, TipoAsistencia


EMPLEADOS_DATA = [{'nombres': 'Claudia', 'apellidos': 'Aguilar'}, {'nombres': 'Ademir', 'apellidos': 'Arredondo'}, {'nombres': 'Jonathan Oswaldo', 'apellidos': 'Azaña Ramos'}, {'nombres': 'Jose Angel', 'apellidos': 'Borda Hernandez'}, {'nombres': 'Valery', 'apellidos': 'Celestino Begar'}, {'nombres': 'Edwin', 'apellidos': 'Chaparro Ampa'}, {'nombres': 'Jose Alberto', 'apellidos': 'Davila Paredes'}, {'nombres': 'Jean Leonardo', 'apellidos': 'Estrada Roque'}, {'nombres': 'Marco Antonio Jose', 'apellidos': 'Garcia Galvan'}, {'nombres': 'Thalia', 'apellidos': 'Giral Onton'}, {'nombres': 'Jose Luis', 'apellidos': 'Gonzalez Romero'}, {'nombres': 'Pedro Luis', 'apellidos': 'Hernandez Reyes'}, {'nombres': 'Edson Pavel', 'apellidos': 'Ipenza'}, {'nombres': 'Joel Edwin', 'apellidos': 'Llanos Mejico'}, {'nombres': 'Carlos Fernando', 'apellidos': 'Lozano Roman'}, {'nombres': 'Carlos Gabriel', 'apellidos': 'More Miranda'}, {'nombres': 'Willy Jhon', 'apellidos': 'Paco Deza'}, {'nombres': 'David Eduardo', 'apellidos': 'Pauta Juarez'}, {'nombres': 'Julio Daniel', 'apellidos': 'Peñaherrera Orrillo'}, {'nombres': 'Jordi Cesar Hernando', 'apellidos': 'Quezada Rosales'}, {'nombres': 'Wilmer', 'apellidos': 'Quispe Huaringa'}, {'nombres': 'Cecy Kattia', 'apellidos': 'Salcedo Arauda'}, {'nombres': 'Jose Lino', 'apellidos': 'Solano Caqui'}, {'nombres': 'Jaime Franksue', 'apellidos': 'Sullon Li'}, {'nombres': 'Yuli', 'apellidos': 'Tarazona'}, {'nombres': 'Alexis', 'apellidos': 'Vasquez Conchatupac'}, {'nombres': 'Zhihua Santiago', 'apellidos': 'Yong Sanchez'}]

TIPOS_ASISTENCIA = ['Entrada', 'Salida', 'Inicio Almuerzo', 'Fin Almuerzo', 'Entrada por comisión', 'Salida por comisión', 'Entrada por otros', 'Salida por otros']


class Command(BaseCommand):
    help = "Carga empleados y tipos de asistencia iniciales (idempotente)."

    def handle(self, *args, **options):
        sorted_empleados = sorted(
            EMPLEADOS_DATA,
            key=lambda e: (e["apellidos"].lower(), e["nombres"].lower()),
        )
        for emp in sorted_empleados:
            Empleado.objects.get_or_create(
                nombres=emp["nombres"],
                apellidos=emp["apellidos"],
            )
        self.stdout.write(self.style.SUCCESS(f"Empleados: {len(sorted_empleados)} procesados."))

        for nombre in TIPOS_ASISTENCIA:
            TipoAsistencia.objects.get_or_create(nombre_asistencia=nombre)
        self.stdout.write(self.style.SUCCESS(f"Tipos de asistencia: {len(TIPOS_ASISTENCIA)} creados."))
        self.stdout.write(self.style.SUCCESS("Datos cargados correctamente."))
