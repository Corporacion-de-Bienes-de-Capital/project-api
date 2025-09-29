from django.db import models
from project.infrastructure.django_models.proyecto import ProyectoORM

class BitacorasORM(models.Model):
    bita_id = models.AutoField(primary_key=True)
    bita_inversion = models.TextField(null=True, blank=True)
    bita_cronograma = models.TextField(null=True, blank=True)
    bita_estado_sea = models.TextField(null=True, blank=True)
    bita_otros = models.TextField(null=True, blank=True)
    is_deleted = models.IntegerField(null=True, blank=True)
    created_at = models.IntegerField(null=True, blank=True)
    edited_at = models.IntegerField(null=True, blank=True)
    user_created_at = models.CharField(max_length=150, null=True, blank=True)
    user_edited_at = models.CharField(max_length=150, null=True, blank=True)
    
    pro = models.ForeignKey(
        ProyectoORM,
        db_column='pro_id',
        on_delete=models.DO_NOTHING,
        related_name='bitacoras'
    )

    class Meta:
        db_table = 'tbl_bitacoras'
        managed = False