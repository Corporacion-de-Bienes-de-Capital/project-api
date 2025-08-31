from django.db import models

class TipoInversionORM(models.Model):
    tinv_id = models.AutoField(primary_key=True)
    tinv_nombre = models.CharField(max_length=150, null=True, blank=True)
    oinv_id = models.IntegerField(null=True, blank=True)
    is_deleted = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.PositiveIntegerField(null=True, blank=True)
    edited_at = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_tipo_inversion'
        managed = False

