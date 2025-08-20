from django.db import models

class EstadoProyectoORM(models.Model):
    pro_estado = models.AutoField(primary_key=True)
    estado_nombre = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.IntegerField(default=0)

    class Meta:
        db_table = 'tbl_estado_proyecto'
        managed = False