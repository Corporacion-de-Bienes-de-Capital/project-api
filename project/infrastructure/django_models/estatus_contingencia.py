from django.db import models


class EstatusContingenciaORM(models.Model):
    estatus_cont_id = models.AutoField(primary_key=True)
    estatus_cont_nombre = models.CharField(max_length=255, null=True, blank=True)
    

    class Meta:
        db_table = 'tbl_estatus_contingencia'
        managed = False