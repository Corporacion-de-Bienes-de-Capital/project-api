from django.db import models

class PaisORM(models.Model):
    pais_id = models.AutoField(primary_key=True)
    pais_nombre = models.CharField(max_length=150, null=True, blank=True)
    pais_codigo = models.CharField(max_length=6, null=True, blank=True)
    pais_flag = models.CharField(max_length=50, null=True, blank=True)
    is_deleted = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.PositiveIntegerField(null=True, blank=True)
    edited_at = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_pais'
        managed = False
