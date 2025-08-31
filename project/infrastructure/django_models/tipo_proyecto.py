from django.db import models


class TipoProyectoORM(models.Model):
    tpro_id = models.AutoField(primary_key=True)
    tpro_nombre = models.CharField(max_length=150, null=True, blank=True)
    is_deleted = models.PositiveSmallIntegerField(null=True, blank=True)
    
    

    class Meta:
        db_table = 'tbl_tipo_proyecto'
        managed = False