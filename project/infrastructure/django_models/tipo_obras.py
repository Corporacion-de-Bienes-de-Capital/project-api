from django.db import models

class TipoObraORM(models.Model):
    tiob_id = models.AutoField(primary_key=True)
    tiob_nombre = models.CharField(max_length=200, null=True, blank=True)
    is_deleted = models.IntegerField(null=True, blank=True)
    created_at = models.IntegerField(null=True, blank=True)
    edited_at = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_tipo_obras'
        managed = False