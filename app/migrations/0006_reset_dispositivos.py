from django.db import migrations


def reset_dispositivos(apps, schema_editor):
    DispositivoEmpleado = apps.get_model('app', 'DispositivoEmpleado')
    DispositivoEmpleado.objects.all().delete()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_actividadproyecto'),
    ]

    operations = [
        migrations.RunPython(reset_dispositivos, noop),
    ]
