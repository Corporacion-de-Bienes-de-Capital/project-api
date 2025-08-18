from django.db import models

class EmpresaORM(models.Model):
    empr_id = models.AutoField(primary_key=True)
    empr_nombre = models.CharField(max_length=255, null=True, blank=True)
    empr_rut = models.CharField(max_length=30)
    empr_razon_social = models.CharField(max_length=255, null=True, blank=True)
    empr_ciudad = models.CharField(max_length=50, null=True, blank=True)
    empr_direccion = models.CharField(max_length=150, null=True, blank=True)
    empr_telefono = models.CharField(max_length=60, null=True, blank=True)
    empr_fax = models.CharField(max_length=20, null=True, blank=True)
    empr_correo_principal = models.CharField(max_length=150, null=True, blank=True)
    empr_observacion = models.CharField(max_length=255, null=True, blank=True)
    empr_no_inscrita = models.IntegerField(default=0)
    pais_id = models.IntegerField(null=True, blank=True)
    comu_id = models.CharField(max_length=40, null=True, blank=True)
    aeco_id = models.IntegerField(null=True, blank=True)
    is_active = models.PositiveIntegerField(default=1)
    is_deleted = models.PositiveIntegerField(default=0)
    created_at = models.PositiveIntegerField(null=True, blank=True)
    edited_at = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_empresas'
        managed = False