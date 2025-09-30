from django.db import models
from .proyecto import ProyectoORM

class EtapasProyectoORM(models.Model):
    pro = models.OneToOneField(ProyectoORM, primary_key=True, on_delete=models.CASCADE, db_column='pro_id')
    ing_conc_inicio = models.DateField(null=True, blank=True)
    ing_conc_fin = models.DateField(null=True, blank=True)
    ing_basica_inicio = models.DateField(null=True, blank=True)
    ing_basica_fin = models.DateField(null=True, blank=True)
    ing_detalle_inicio = models.DateField(null=True, blank=True)
    ing_detalle_fin = models.DateField(null=True, blank=True)
    cons_inicio = models.DateField(null=True, blank=True)
    cons_fin = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_etapas_proyecto'