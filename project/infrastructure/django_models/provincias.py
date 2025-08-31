from django.db import models


class ProvinciasORM(models.Model):
    prov_id = models.AutoField(primary_key=True)
    prov_nombre = models.CharField(max_length=150, null=True, blank=True)
    prov_codigo = models.CharField(max_length=10, null=True, blank=True)
    is_deleted = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.PositiveIntegerField(null=True, blank=True)

    reg_id = models.ForeignKey(
        'RegionORM',
        on_delete=models.DO_NOTHING,
        db_column='reg_id',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'tbl_provincias'
        managed = False