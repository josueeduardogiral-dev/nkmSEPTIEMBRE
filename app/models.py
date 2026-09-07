from django.db import models
from django.utils import timezone
from datetime import date

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    codigo_qr = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del empleado."""
        return f"{self.nombres} {self.apellidos}"
    
    def tiene_registro_hoy(self, tipo_asistencia):
        """
        Verifica si el empleado tiene un registro del tipo especificado hoy.
        
        Args:
            tipo_asistencia: Instancia de TipoAsistencia
            
        Returns:
            bool: True si tiene el registro hoy
        """
        hoy = timezone.localtime().date()
        return self.registroasistencia_set.filter(
            tipo=tipo_asistencia,
            fecha_registro=hoy
        ).exists()
    
    def obtener_registros_hoy(self):
        """Obtiene todos los registros del empleado para hoy."""
        hoy = timezone.localtime().date()
        return self.registroasistencia_set.filter(fecha_registro=hoy).order_by('hora_registro')
    
    def generar_codigo_qr(self):
        """
        Genera un código QR único para el empleado si no existe.
        
        Returns:
            str: Código QR generado
        """
        if not self.codigo_qr:
            import uuid
            # Generar código único basado en ID y timestamp
            codigo = f"EMP{self.id_empleado}{uuid.uuid4().hex[:8].upper()}"
            self.codigo_qr = codigo
            self.save()
        return self.codigo_qr
    
    @classmethod
    def buscar_por_codigo_qr(cls, codigo):
        """
        Busca un empleado por su código QR.
        
        Args:
            codigo: Código QR a buscar
            
        Returns:
            Empleado o None si no se encuentra
        """
        try:
            return cls.objects.get(codigo_qr=codigo)
        except cls.DoesNotExist:
            return None

class DispositivoEmpleado(models.Model):
    """Vincula un dispositivo (fingerprint) con un empleado para auto-identificación."""
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fingerprint = models.CharField(max_length=100, unique=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.empleado.nombre_completo} - {self.fingerprint}"

    @classmethod
    def obtener_empleado_por_fingerprint(cls, fp):
        try:
            vinculo = cls.objects.select_related('empleado').get(fingerprint=fp)
            return vinculo.empleado
        except cls.DoesNotExist:
            return None

class TipoAsistencia(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre_asistencia = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_asistencia
    
    @property
    def es_tipo_unico(self):
        """
        Verifica si este tipo de asistencia solo puede registrarse una vez por día.
        
        Returns:
            bool: True si es un tipo único
        """
        tipos_unicos = ['Entrada', 'Inicio Almuerzo', 'Fin Almuerzo', 'Salida']
        return self.nombre_asistencia in tipos_unicos
    
    @property
    def requiere_descripcion(self):
        """
        Verifica si este tipo de asistencia requiere descripción adicional.
        
        Returns:
            bool: True si requiere descripción
        """
        tipos_con_descripcion = ['Entrada por otros', 'Salida por otros']
        return self.nombre_asistencia in tipos_con_descripcion

class RegistroAsistencia(models.Model):
    id_registro = models.AutoField(primary_key=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoAsistencia, on_delete=models.CASCADE)
    fecha_registro = models.DateField()
    hora_registro = models.TimeField()
    descripcion = models.CharField(max_length=50, blank=True, null=True)   
    fingerprint = models.CharField(max_length=100, blank=True, null=True) # FingerprintJS ID del dispositivo

    def __str__(self):
        return f"{self.empleado} - {self.tipo.nombre_asistencia} - {self.fecha_registro} {self.hora_registro}"
    
    @property
    def fecha_hora_completa(self):
        """Retorna la fecha y hora combinadas como string."""
        return f"{self.fecha_registro} {self.hora_registro}"
    
    @property
    def es_registro_hoy(self):
        """Verifica si el registro es de hoy."""
        hoy = timezone.localtime().date()
        return self.fecha_registro == hoy
    
    @classmethod
    def obtener_registros_hoy(cls):
        """Obtiene todos los registros de hoy."""
        hoy = timezone.localtime().date()
        return cls.objects.filter(fecha_registro=hoy).select_related('empleado', 'tipo')
    
    @classmethod
    def obtener_registros_por_empleado(cls, empleado, fecha=None):
        """
        Obtiene registros de un empleado para una fecha específica.
        
        Args:
            empleado: Instancia de Empleado
            fecha: Fecha específica (opcional, por defecto hoy)
            
        Returns:
            QuerySet: Registros del empleado
        """
        if fecha is None:
            fecha = timezone.localtime().date()
        
        return cls.objects.filter(
            empleado=empleado,
            fecha_registro=fecha
        ).select_related('tipo').order_by('hora_registro')

class ActividadProyecto(models.Model):
    """Registro local de proyecto y actividad declarada por el empleado. Solo una vez por día (al registrar Entrada)."""
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    proyecto = models.CharField(max_length=100)
    actividad = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["empleado", "fecha"], name="uniq_actividadpor_dia")
        ]

    def __str__(self):
        return f"{self.empleado.nombre_completo} - {self.proyecto} / {self.actividad} - {self.fecha} {self.hora}"
