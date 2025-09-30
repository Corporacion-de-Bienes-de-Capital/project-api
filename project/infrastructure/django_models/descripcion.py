from django.db import models
from project.infrastructure.django_models.proyecto import ProyectoORM

class DescripcionORM(models.Model):
    desc_id = models.AutoField(primary_key=True)
    
    desc_objetivo = models.TextField(null=True, blank=True)
    desc_resumen = models.TextField(null=True, blank=True)  
    is_deleted = models.BooleanField(null=True, blank=True)
    created_at = models.IntegerField(null=True, blank=True)
    edited_at = models.IntegerField(null=True, blank=True)
    desc_ubicacion = models.TextField(null=True, blank=True)
    desc_vidautil = models.TextField(null=True, blank=True)
    desc_obras = models.TextField(null=True, blank=True)

    pro = models.ForeignKey(
        ProyectoORM,
        db_column='pro_id',
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        related_name='descripciones'
    )

    class Meta:
        db_table = 'tbl_descripcion'
        managed = False