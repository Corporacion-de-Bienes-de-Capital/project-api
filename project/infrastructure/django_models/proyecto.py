from django.db import models
from .empresa import EmpresaORM
from .estado_pro import EstadoProyectoORM 
from project.infrastructure.django_models.tipo_inversion import TipoInversionORM
from project.infrastructure.django_models.tipologias import TipologiasORM
from project.infrastructure.django_models.sector_economico import SectorEconomicoORM
from project.infrastructure.django_models.tipo_proyecto import TipoProyectoORM
from project.infrastructure.django_models.generacion_distribuida import GeneracionDistribuidaORM
from project.infrastructure.django_models.relacion_hidrogeno import RelacionHidrogenoORM 
from project.infrastructure.django_models.estatus_contingencia import EstatusContingenciaORM   
from project.infrastructure.django_models.pais import PaisORM
from project.infrastructure.django_models.region import RegionORM
from project.infrastructure.django_models.provincias import ProvinciasORM
from project.infrastructure.django_models.comunas import ComunasORM

class ProyectoORM(models.Model):
    pro_id = models.AutoField(primary_key=True)
    pro_nombre = models.TextField(null=True, blank=True)
    pro_producto = models.CharField(max_length=255, null=True, blank=True)
    pro_capacidad_produccion = models.CharField(max_length=255, null=True, blank=True)
    pro_ubicacion = models.TextField(null=True, blank=True)
    region_incidencia_proyecto = models.TextField(null=True, blank=True)
    pro_monto_inversion = models.FloatField(null=True, blank=True)
    pro_descripcion = models.TextField(null=True, blank=True)
    is_covid_affected = models.IntegerField(default=0)
    is_green_hydrogen = models.IntegerField(default=0)
    relacion_hidrogeno_id = models.IntegerField(null=True, blank=True)
    is_deleted = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.PositiveIntegerField(null=True, blank=True)
    edited_at = models.PositiveIntegerField(null=True, blank=True)
    user_created_at = models.IntegerField(null=True, blank=True)
    user_edited_at = models.IntegerField(null=True, blank=True)
    comu_id = models.TextField(null=True, blank=True)
    pro_cron_fecha = models.IntegerField(null=True, blank=True)
    pro_diferido = models.IntegerField(default=0)
    confidencial = models.IntegerField(default=0)
    mindha = models.IntegerField(null=True, blank=True)
    sea_afectado = models.IntegerField(null=True, blank=True)
    desaladora = models.IntegerField(default=0)
    codigo_bip = models.CharField(max_length=255, null=True, blank=True)
    codigo_sea = models.CharField(max_length=50, null=True, blank=True)

    # Relación con estado de proyecto
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
        null=True,
        blank=True
    )

    # Relación con tipo de inversión
    tinv_id = models.ForeignKey(
        'TipoInversionORM',
        on_delete=models.DO_NOTHING,
        db_column='tinv_id',
        null=True,
        blank=True
    )

    #Relación con sector económico
    seco_id = models.ForeignKey(
        'SectorEconomicoORM',
        on_delete=models.DO_NOTHING,
        db_column='seco_id',
        null=True,
        blank=True
    )

    #Relación con tipologías
    tplo_id = models.ForeignKey(
        'TipologiasORM',
        on_delete=models.DO_NOTHING,
        db_column='tplo_id',
        null=True,
        blank=True
    )

    #Relacion con tipo de proyecto
    tpro_id = models.ForeignKey(
        'TipoProyectoORM',
        on_delete=models.DO_NOTHING,
        db_column='tpro_id',
        null=True,
        blank=True
    )

    #Relación con generación distribuida
    dist_id = models.ForeignKey(
        'GeneracionDistribuidaORM',
        on_delete=models.DO_NOTHING,
        db_column='dist_id',
        null=True,
        blank=True
    )


    #Relación con hidrógeno
    relacion_hidrogeno_id = models.ForeignKey(
        'RelacionHidrogenoORM',
        on_delete=models.DO_NOTHING,
        db_column='relacion_hidrogeno_id',
        null=True,
        blank=True
    )

    #Relacion con Estatus Contingencia
    estatus_cont_id = models.ForeignKey(
        'EstatusContingenciaORM',
        on_delete=models.DO_NOTHING,
        db_column='estatus_cont_id',
        null=True,
        blank=True
    )

    #Relacion con pais
    pais_id = models.ForeignKey(
        'PaisORM',
        on_delete=models.DO_NOTHING,
        db_column='pais_id',
        null=True,
        blank=True
    )

    #Relacion con region
    reg_id = models.ForeignKey(
        'RegionORM',
        on_delete=models.DO_NOTHING,
        db_column='reg_id',
        null=True,
        blank=True
    ) 

    #Relacion con provincia
    prov_id = models.ForeignKey(
        'ProvinciasORM',
        on_delete=models.DO_NOTHING,
        db_column='prov_id',
        null=True,
        blank=True
    )

    #Relación con comuna
    comu_id = models.ForeignKey(
        'ComunasORM',
        on_delete=models.DO_NOTHING,  
        db_column='comu_id',
        null=True,
        blank=True
    )
                          


    class Meta:
        db_table = 'tbl_proyecto'
        managed = False