from django.db import models


class RelacionHidrogenoORM(models.Model):
    relacion_hidrogeno_id = models.AutoField(primary_key=True)
    relacion_hidrogeno_nombre = models.CharField(max_length=40, null=True)

    class Meta:
        db_table = 'tbl_relacion_hidrogeno'
        managed = False