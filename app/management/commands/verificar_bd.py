"""Read-only database diagnostic without exposing credentials."""
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, DatabaseError


class Command(BaseCommand):
    help = 'Verifica PostgreSQL y cuenta empleados sin modificar datos ni mostrar claves.'

    def add_arguments(self, parser):
        parser.add_argument('--solo-conexion', action='store_true')

    def handle(self, *args, **options):
        if connection.vendor != 'postgresql':
            raise CommandError('Se requiere PostgreSQL. No se permite una base local SQLite.')
        self.stdout.write('Servidor PostgreSQL: ' + connection.settings_dict.get('HOST', ''))
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
        except DatabaseError:
            raise CommandError(
                'No se pudo conectar a PostgreSQL. Revisa el proyecto Supabase, '
                'su estado, el host del Session pooler, usuario, contrasena y acceso de red. '
                'No se usara una base local.'
            ) from None
        self.stdout.write(self.style.SUCCESS('Conexion PostgreSQL/SSL: OK'))
        if options['solo_conexion']:
            return
        from app.models import Empleado
        try:
            count = Empleado.objects.count()
        except DatabaseError:
            raise CommandError(
                'La conexion funciona, pero no se pudo consultar empleados. '
                'Revisa las migraciones y permisos de las tablas.'
            ) from None
        self.stdout.write(f'Empleados registrados: {count}')
        if count == 0:
            self.stdout.write(self.style.WARNING(
                'Base sin empleados: confirma que sea el proyecto correcto. '
                'Para cargar la lista incluida ejecuta: python manage.py cargar_empleados'
            ))
