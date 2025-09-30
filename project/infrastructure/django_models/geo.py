from django.db import models
from .proyecto import ProyectoORM

class GeoORM(models.Model):
    pro = models.OneToOneField(ProyectoORM, primary_key=True, on_delete=models.CASCADE, db_column='pro_id')
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    created_at = models.BigIntegerField(null=True, blank=True)
    edited_at = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_geo'
