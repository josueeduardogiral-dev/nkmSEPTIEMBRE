from datetime import date
import os
import unittest

os.environ.setdefault(
    'DATABASE_URL',
    'postgresql://test:test@example.invalid:5432/postgres',
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_asistencia.settings')

import django
django.setup()

import openpyxl
from io import BytesIO
from unittest.mock import patch
from django.urls import resolve, reverse
from app.services import ReporteService
from app.views import _nombre_hoja_empleado, exportar_reporte_mensual_empleados


class MonthlyReportTests(unittest.TestCase):
    def test_weeks_are_four_monday_to_friday_blocks(self):
        ranges = ReporteService.rangos_semanales_mes(date(2026, 8, 31))
        self.assertEqual(
            ranges,
            [
                (1, date(2026, 8, 3), date(2026, 8, 7)),
                (2, date(2026, 8, 10), date(2026, 8, 14)),
                (3, date(2026, 8, 17), date(2026, 8, 21)),
                (4, date(2026, 8, 24), date(2026, 8, 28)),
            ],
        )

    def test_february_still_uses_four_work_weeks(self):
        ranges = ReporteService.rangos_semanales_mes(date(2024, 2, 10))
        self.assertEqual(ranges[-1], (4, date(2024, 2, 26), date(2024, 2, 29)))

    def test_excel_sheet_names_are_valid_and_unique(self):
        empleado = type('Empleado', (), {
            'nombre_completo': 'Nombre / muy largo : para [Excel] empleado repetido',
            'pk': 1,
        })()
        usados = set()
        primero = _nombre_hoja_empleado(empleado, usados)
        segundo = _nombre_hoja_empleado(empleado, usados)
        self.assertLessEqual(len(primero), 31)
        self.assertNotEqual(primero, segundo)
        self.assertFalse(any(char in primero for char in '[]:*?/\\'))

    @patch('app.views.RegistroAsistencia.objects')
    @patch('app.views.Empleado.objects')
    def test_empty_database_still_generates_valid_workbook(self, empleados, registros):
        empleados.order_by.return_value = []
        registros.filter.return_value.select_related.return_value.order_by.return_value = []
        undecorated = exportar_reporte_mensual_empleados.__wrapped__
        response = undecorated(object())
        workbook = openpyxl.load_workbook(BytesIO(response.content))
        self.assertEqual(workbook.sheetnames, ['Sin empleados'])
        self.assertIn('No hay empleados', workbook.active['A1'].value)

    def test_existing_attendance_download_uses_monthly_report(self):
        url = reverse('descargar_excel')
        self.assertEqual(url, '/login/descargar/asistencia')
        self.assertIs(resolve(url).func, exportar_reporte_mensual_empleados)


if __name__ == '__main__':
    unittest.main()
