

from django.db import models
from project.infrastructure.django_models.proyecto import ProyectoORM

class RelListadoEquiposDescripcionORM(models.Model):
    lieq_id = models.IntegerField(primary_key=True)
    pro = models.ForeignKey(ProyectoORM, db_column='pro_id', on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(null=True, blank=True)
    created_at = models.IntegerField(null=True, blank=True)
    edited_at = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'rel_listado_equipos_descripcion'
        managed = False
        unique_together = (('lieq_id', 'pro'),)