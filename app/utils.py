"""
Utilidades comunes para el sistema de asistencia.
Funciones auxiliares que pueden ser reutilizadas.
"""

from datetime import datetime, timedelta
from django.utils import timezone


def obtener_fecha_hora_actual():
    """
    Obtiene la fecha y hora actual en la zona horaria configurada.
    
    Returns:
        tuple: (fecha, hora) como objetos date y time
    """
    now = timezone.localtime()
    return now.date(), now.time()


def formatear_timedelta(td):
    """
    Convierte un timedelta a formato HH:MM.
    
    Args:
        td: timedelta object
        
    Returns:
        str: Formato HH:MM
    """
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{hours:02d}:{minutes:02d}"


def calcular_distancia_geografica(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos geográficos en metros.
    Usa la fórmula de Haversine.
    
    Args:
        lat1, lon1: Coordenadas del primer punto
        lat2, lon2: Coordenadas del segundo punto
        
    Returns:
        float: Distancia en metros
    """
    import math
    
    R = 6371000  # Radio de la Tierra en metros
    rad = math.pi / 180
    
    d_lat = (lat2 - lat1) * rad
    d_lon = (lon2 - lon1) * rad
    
    a = (math.sin(d_lat/2)**2 + 
         math.cos(lat1*rad) * math.cos(lat2*rad) * math.sin(d_lon/2)**2)
    
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def validar_ubicacion_empresa(lat, lon, lat_empresa=-12.080257055918374, lon_empresa=-76.99778307088776, radio=500):
    """
    Valida si las coordenadas están dentro del radio de la empresa.
    
    Args:
        lat, lon: Coordenadas a validar
        lat_empresa, lon_empresa: Coordenadas de la empresa
        radio: Radio permitido en metros
        
    Returns:
        bool: True si está dentro del radio
    """
    distancia = calcular_distancia_geografica(lat, lon, lat_empresa, lon_empresa)
    return distancia <= radio


def obtener_tipos_asistencia_unicos():
    """
    Retorna la lista de tipos de asistencia que solo pueden registrarse una vez por día.
    
    Returns:
        list: Lista de nombres de tipos únicos
    """
    return ['Entrada', 'Inicio Almuerzo', 'Fin Almuerzo', 'Salida']


def obtener_tipos_asistencia_con_descripcion():
    """
    Retorna la lista de tipos de asistencia que requieren descripción adicional.
    
    Returns:
        list: Lista de nombres de tipos con descripción
    """
    return ['Entrada por otros', 'Salida por otros']
