from django.db import models

class GeneracionDistribuidaORM(models.Model):
    dist_id = models.AutoField(primary_key=True)
    dist_nombre = models.CharField(max_length=150, null=True, blank=True)


    class Meta:
        db_table = 'tbl_generacion_distribuida'
        managed = False