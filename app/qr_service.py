"""
Servicio para manejar el sistema de códigos QR.
Permite identificación automática de empleados mediante QR.
"""

import qrcode
import os
from django.conf import settings
from django.http import JsonResponse
from .models import Empleado


class QRService:
    """Servicio para manejar códigos QR de empleados."""
    
    @staticmethod
    def generar_qr_empleado(empleado):
        """
        Genera un código QR para un empleado específico.
        
        Args:
            empleado: Instancia de Empleado
            
        Returns:
            str: Ruta del archivo QR generado
        """
        # Generar código QR si no existe
        codigo_qr = empleado.generar_codigo_qr()
        
        # URL que se codificará en el QR
        base_url = os.getenv("APP_URL", "http://127.0.0.1:8000")
        qr_url = f"{base_url}/qr/{codigo_qr}/"
        
        # Crear directorio si no existe
        qr_dir = os.path.join(settings.BASE_DIR, 'qr_codes')
        os.makedirs(qr_dir, exist_ok=True)
        
        # Generar QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)
        
        # Crear imagen
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Guardar archivo
        filename = f"qr_{empleado.id_empleado}_{codigo_qr}.png"
        filepath = os.path.join(qr_dir, filename)
        img.save(filepath)
        
        return filepath
    
    @staticmethod
    def generar_qr_todos_empleados():
        """
        Genera códigos QR para todos los empleados.
        
        Returns:
            list: Lista de rutas de archivos generados
        """
        empleados = Empleado.objects.all()
        archivos_generados = []
        
        for empleado in empleados:
            try:
                archivo = QRService.generar_qr_empleado(empleado)
                archivos_generados.append({
                    'empleado': empleado,
                    'archivo': archivo,
                    'codigo_qr': empleado.codigo_qr
                })
            except Exception as e:
                print(f"Error generando QR para {empleado}: {e}")
        
        return archivos_generados
    
    @staticmethod
    def buscar_empleado_por_qr(codigo_qr):
        """
        Busca un empleado por su código QR.
        
        Args:
            codigo_qr: Código QR escaneado
            
        Returns:
            dict: Respuesta con empleado encontrado o error
        """
        try:
            empleado = Empleado.buscar_por_codigo_qr(codigo_qr)
            
            if empleado:
                return {
                    'success': True,
                    'empleado': {
                        'id': empleado.id_empleado,
                        'nombres': empleado.nombres,
                        'apellidos': empleado.apellidos,
                        'nombre_completo': empleado.nombre_completo
                    }
                }
            else:
                return {
                    'success': False,
                    'error': 'Empleado no encontrado'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al buscar empleado: {str(e)}'
            }
    
    @staticmethod
    def obtener_url_qr_empleado(empleado):
        """
        Obtiene la URL del QR para un empleado.
        
        Args:
            empleado: Instancia de Empleado
            
        Returns:
            str: URL del QR
        """
        codigo_qr = empleado.generar_codigo_qr()
        base_url = os.getenv("APP_URL", "http://127.0.0.1:8000")
        return f"{base_url}/qr/{codigo_qr}/"
