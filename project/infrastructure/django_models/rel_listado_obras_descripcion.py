from django.db import models
from project.infrastructure.django_models.proyecto import ProyectoORM


class RelListadoObrasDescripcionORM(models.Model):
    liob_id = models.IntegerField(primary_key=True)
    pro = models.ForeignKey(
        ProyectoORM, db_column='pro_id', on_delete=models.DO_NOTHING
    )
    created_at = models.IntegerField(null=True, blank=True)
    edited_at = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'rel_listado_obras_descripcion'
        managed = False
        unique_together = (('liob_id', 'pro'),)
