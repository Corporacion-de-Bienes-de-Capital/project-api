from django.db import models


class ComunasORM(models.Model):
    comu_id = models.AutoField(primary_key=True)
    comu_nombre = models.CharField(max_length=150, null=True, blank=True)
    comu_codigo = models.CharField(max_length=150, null=True, blank=True)
    is_deleted = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.PositiveIntegerField(null=True, blank=True)
    edited_at = models.PositiveIntegerField(null=True, blank=True)

    # Relacion con provincia
    prov_id = models.ForeignKey(
        'ComunasORM',
        on_delete=models.DO_NOTHING,  
        db_column='prov_id',
    )

    class Meta:
        db_table = 'tbl_comunas'
        managed = False