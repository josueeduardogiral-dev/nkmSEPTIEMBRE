from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.pagina_principal, name='pagina_principal'),
    
    # Paso previo: Control de Actividades
    path('actividades/<int:empleado_id>/', views.control_actividades, name='control_actividades'),

    # Sistema tradicional (mantenido para compatibilidad)
    path('manual/', views.registrar_asistencia, name='registrar_asistencia'),
    
    # Sistema de QR por empleado (existente)
    path('qr/', views.escanear_qr, name='escanear_qr'),
    path('qr/<str:codigo_qr>/', views.registrar_asistencia_qr, name='registrar_asistencia_qr'),
    path('api/buscar-empleado-qr/', views.api_buscar_empleado_qr, name='api_buscar_empleado_qr'),

    # QR general: auto-identificación por dispositivo
    path('auto/', views.identificar_dispositivo, name='identificar_dispositivo'),
    path('auto/empleado/<int:empleado_id>/', views.registrar_asistencia_auto, name='registrar_asistencia_auto'),
    path('api/identificar-fingerprint/', views.api_identificar_por_fingerprint, name='api_identificar_por_fingerprint'),
    path('api/vincular-fingerprint/', views.api_vincular_fingerprint, name='api_vincular_fingerprint'),
    path('api/desvincular-fingerprint/', views.api_desvincular_fingerprint, name='api_desvincular_fingerprint'),
    
    # Reportes (solo para staff)
    path('login/descarga/', views.pagina_descarga_excel, name='pagina_descarga_excel'),
    path('login/descargar/asistencia', views.exportar_reporte_mensual_empleados, name='descargar_excel'),
    path('login/descargar/resumen/', views.exportar_resumen_excel, name='resumen_excel'),
]
