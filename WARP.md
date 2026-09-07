# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project overview
- Django app for tracking employee attendance with optional device fingerprint validation and Excel exports. Core app is app; project module is control_asistencia.

Common commands
- Create venv (PowerShell):
  - python -m venv .venv
  - .\.venv\Scripts\Activate.ps1
- Install deps: pip install -r requirements.txt
- Migrations: python manage.py migrate
- Create admin/staff user: python manage.py createsuperuser
- Load example data: python cargar_empleados.py
- Run dev server: python manage.py runserver
- Production (Procfile): web: bash start.sh
- Run all tests: python manage.py test
- Run a single test (no tests included yet; example): python manage.py test app.tests.AlgunaPrueba.test_caso

Key URLs
- Formulario principal: /
- Sistema tradicional (compatibilidad): /manual/
- QR por empleado: /qr/ y /qr/<codigo_qr>/
- QR general (auto-identificación por dispositivo): /auto/
- API identificar por fingerprint: POST /api/identificar-fingerprint/
- API vincular fingerprint: POST /api/vincular-fingerprint/
- Login (Django auth): /login/
- Página de descargas (requiere is_staff): /login/descarga/
- Exportar asistencia (detalle): /login/descargar/asistencia
- Exportar resumen diario: /login/descargar/resumen/

Configuration notes
- Environment via .env or Railway service variables. DATABASE_URL is mandatory (PostgreSQL with SSL); SQLite and DB_LIVE fallbacks are removed. Timezone America/Lima. Static served with WhiteNoise in production.

High-level architecture
- control_asistencia/
  - settings.py: env-driven DB config (PostgreSQL only), ALLOWED_HOSTS/CSRF_TRUSTED_ORIGINS, TIME_ZONE=America/Lima, WhiteNoise for static.
  - urls.py: mounts admin, login view (templated), and includes app.urls.
- app/
  - models.py:
    - Empleado: identidad del trabajador, soporte para generar y almacenar un codigo_qr único.
    - TipoAsistencia: catálogo de eventos; propiedad es_tipo_unico para eventos 1 vez/día.
    - RegistroAsistencia: registro diario con fecha/hora, descripción opcional y fingerprint opcional.
    - DispositivoEmpleado: mapea un fingerprint de dispositivo a un Empleado para auto-identificación.
  - services.py:
    - AsistenciaService:
      - validar_registro_duplicado: evita repetir tipos únicos (Entrada, Inicio Almuerzo, Fin Almuerzo, Salida) en un mismo día.
      - validar_fingerprint_unico: impide usar el mismo fingerprint para distintos empleados en el día; NO bloquea si el fingerprint falta.
      - crear_registro_asistencia: orquesta validaciones y persiste el registro con timezone.localtime.
    - ReporteService:
      - obtener_datos_resumen: consolida registros por empleado/fecha.
      - calcular_horas_empleado: calcula almuerzo, comisión, permisos y trabajadas; búsquedas case-insensitive para nombres de tipos.
  - views.py:
    - Flujos de registro:
      - registrar_asistencia (tradicional: selecciona empleado y tipo).
      - registrar_asistencia_qr (por código QR del empleado).
      - identificar_dispositivo y registrar_asistencia_auto (QR general con fingerprint; permite primer vínculo del dispositivo).
    - Exportaciones Excel: exportar_asistencia_excel (detalle) y exportar_resumen_excel (resumen). Sólo accesibles a staff via login.
  - urls.py: rutas para los flujos anteriores y APIs de fingerprint/QR.
  - qr_service.py: genera/recupera URLs y PNGs de códigos QR por empleado.
  - utils.py: utilidades de tiempo y geolocalización (opcional), y listas de tipos especiales.
  - templates/ y static/: templates por convención (APP_DIRS). WhiteNoise sirve estáticos en producción.

Development workflow cues
- Business rules centralizadas en services.py; las vistas deben delegar validaciones allí.
- Los nombres de TipoAsistencia deben ser consistentes (p. ej., "Inicio Almuerzo"/"Fin Almuerzo"); ReporteService ya tolera variaciones de mayúsculas.
- fingerprint es opcional; si está presente, se valida exclusividad por día entre empleados.

Excel outputs
- Detalle: Empleado, Tipo, Fecha, Hora, Descripción, ID Dispositivo; ordenado por fecha/hora desc.
- Resumen: por empleado y día, incluye almuerzo, comisión, permiso y horas trabajadas; aplica estilos/tablas con openpyxl.
