#!/usr/bin/env python
"""
Script para eliminar empleados duplicados en la base de datos.
Ejecutar: python eliminar_duplicados.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_asistencia.settings')
django.setup()

from app.models import Empleado
from django.db.models import Count

def eliminar_duplicados():
    """Elimina empleados duplicados, manteniendo solo el primero."""
    print("🔍 Buscando empleados duplicados...")
    
    # Buscar duplicados por nombres y apellidos
    duplicados = (
        Empleado.objects
        .values('nombres', 'apellidos')
        .annotate(count=Count('id_empleado'))
        .filter(count__gt=1)
    )
    
    if not duplicados:
        print("✅ No se encontraron empleados duplicados.")
        return
    
    print(f"⚠️  Se encontraron {len(duplicados)} grupos de empleados duplicados:\n")
    
    total_eliminados = 0
    
    for dup in duplicados:
        nombres = dup['nombres']
        apellidos = dup['apellidos']
        count = dup['count']
        
        print(f"👤 {apellidos}, {nombres} - {count} registros")
        
        # Obtener todos los empleados con estos nombres
        empleados = Empleado.objects.filter(
            nombres=nombres, 
            apellidos=apellidos
        ).order_by('id_empleado')
        
        # Mantener el primero, eliminar los demás
        primero = empleados.first()
        duplicados_a_eliminar = empleados.exclude(id_empleado=primero.id_empleado)
        
        for emp in duplicados_a_eliminar:
            print(f"   ❌ Eliminando ID {emp.id_empleado}")
            emp.delete()
            total_eliminados += 1
    
    print(f"\n✅ Se eliminaron {total_eliminados} empleados duplicados.")
    print(f"📊 Total de empleados ahora: {Empleado.objects.count()}")

if __name__ == "__main__":
    try:
        eliminar_duplicados()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import sys
        sys.exit(1)
