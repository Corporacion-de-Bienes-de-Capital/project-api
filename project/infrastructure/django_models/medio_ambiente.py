from django.db import models
from project.infrastructure.django_models.proyecto import ProyectoORM
from project.infrastructure.django_models.estado_sea import EstadoSeaORM


class MedioAmbienteORM(models.Model):
    mamb_id = models.AutoField(primary_key=True)
    mamb_emp_pres_proyecto = models.CharField(max_length=250, null=True, blank=True)
    mamb_tipo_proyecto = models.CharField(max_length=255, null=True, blank=True)
    mamb_fecha_presentacion = models.IntegerField(null=True, blank=True)
    mamb_contacto = models.CharField(max_length=255, null=True, blank=True)
    mamb_plazo_evaluacion = models.IntegerField(null=True, blank=True)
    mamb_dias_legales = models.CharField(max_length=255, null=True, blank=True)
    mamb_dias_totales = models.CharField(max_length=255, null=True, blank=True)
    ppro_id = models.IntegerField(null=True, blank=True)
    mamb_enlace_sea = models.CharField(max_length=255, null=True, blank=True)
    is_history = models.IntegerField(null=True, blank=True)
    is_deleted = models.IntegerField(null=True, blank=True)
    mamb_fecha_calificacion = models.IntegerField(null=True, blank=True)
    mamb_descripcion = models.TextField(null=True, blank=True)

    # Relación con ProyectoORM
    pro_id = models.ForeignKey(
        ProyectoORM,
        on_delete=models.DO_NOTHING,
        db_column='pro_id',
        related_name='medioambiente' # <-- así defines el nombre
    )

    # Relación con EstadoSeaORM
    esea = models.ForeignKey(
        EstadoSeaORM,
        on_delete=models.DO_NOTHING,
        db_column='esea_id'
    )

    class Meta:
        db_table = 'view_last_medio_ambiente'
        managed = False