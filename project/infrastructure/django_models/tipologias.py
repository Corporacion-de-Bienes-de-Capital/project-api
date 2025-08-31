from django.db import models
from project.infrastructure.django_models.sector_economico import SectorEconomicoORM

class TipologiasORM(models.Model):
    tplo_id = models.AutoField(primary_key=True)
    tplo_nombre = models.CharField(max_length=150, null=True, blank=True)
    tplo_codigo = models.CharField(max_length=150, null=True, blank=True)
    subeco_id = models.IntegerField(null=True, blank=True)   
    is_deleted = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.PositiveIntegerField(null=True, blank=True)
    edited_at = models.PositiveIntegerField(null=True, blank=True)

    # relación con sector económico
    seco_id = models.ForeignKey(
        SectorEconomicoORM,
        on_delete=models.DO_NOTHING,
        db_column='seco_id',
        null=False,
        blank=False
    )

    class Meta:
        db_table = 'tbl_tipologias'
        managed = False
