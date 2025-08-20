from django.db import models
from .empresa import EmpresaORM
from .estado_pro import EstadoProyectoORM 

class ProyectoORM(models.Model):
    pro_id = models.AutoField(primary_key=True)
    pro_nombre = models.TextField(null=True, blank=True)
    pro_producto = models.CharField(max_length=255, null=True, blank=True)
    pro_capacidad_produccion = models.CharField(max_length=255, null=True, blank=True)
    pro_ubicacion = models.TextField(null=True, blank=True)
    region_incidencia_proyecto = models.TextField(null=True, blank=True)
    pro_monto_inversion = models.FloatField(null=True, blank=True)
    pro_descripcion = models.TextField(null=True, blank=True)
    
    tinv_id = models.PositiveIntegerField(null=True, blank=True)
    seco_id = models.PositiveIntegerField(null=True, blank=True)
    tplo_id = models.PositiveIntegerField(null=True, blank=True)
    tpro_id = models.IntegerField(null=True, blank=True)
    dist_id = models.IntegerField(null=True, blank=True)
    estatus_cont_id = models.IntegerField(null=True, blank=True)
    is_covid_affected = models.IntegerField(default=0)
    is_green_hydrogen = models.IntegerField(default=0)
    relacion_hidrogeno_id = models.IntegerField(null=True, blank=True)
    is_deleted = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.PositiveIntegerField(null=True, blank=True)
    edited_at = models.PositiveIntegerField(null=True, blank=True)
    user_created_at = models.IntegerField(null=True, blank=True)
    user_edited_at = models.IntegerField(null=True, blank=True)
    pais_id = models.PositiveIntegerField()
    reg_id = models.TextField(null=True, blank=True)
    prov_id = models.TextField(null=True, blank=True)
    comu_id = models.TextField(null=True, blank=True)
    pro_cron_fecha = models.IntegerField(null=True, blank=True)
    pro_diferido = models.IntegerField(default=0)
    confidencial = models.IntegerField(default=0)
    mindha = models.IntegerField(null=True, blank=True)
    sea_afectado = models.IntegerField(null=True, blank=True)
    desaladora = models.IntegerField(default=0)
    codigo_bip = models.CharField(max_length=255, null=True, blank=True)
    codigo_sea = models.CharField(max_length=50, null=True, blank=True)
    pro_estado = models.ForeignKey(
        EstadoProyectoORM,
        on_delete=models.DO_NOTHING,
        db_column='pro_estado',
        null=True,
        blank=True
    )
    
    # Relación con empresa
    empresa = models.ForeignKey(
        EmpresaORM, 
        on_delete=models.DO_NOTHING, 
        related_name='proyectos',
        db_column='empr_id',
        #to_field='empr_id',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'tbl_proyecto'
        managed = False