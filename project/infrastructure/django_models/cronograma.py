from django.db import models
from project.infrastructure.django_models.contactos import ContactosORM
from project.infrastructure.django_models.tipo_obras import TipoObraORM
from project.infrastructure.django_models.proyecto import ProyectoORM

class CronogramaORM(models.Model):
    cron_id = models.AutoField(primary_key=True)
    cron_obs = models.CharField(max_length=255, null=True, blank=True)
    cron_etapa = models.IntegerField(null=True, blank=True)
    created_at = models.IntegerField(null=True, blank=True)
    edited_at = models.IntegerField(null=True, blank=True)

    tiob = models.ForeignKey(
        TipoObraORM,
        db_column='tiob_id',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name='cronogramas'
    )
    

    cont = models.ForeignKey(
        ContactosORM,
        db_column='cont_id',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name='cronogramas'
    )

    pro = models.ForeignKey(
        ProyectoORM,
        db_column='pro_id',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name='cronogramas'
    )

    class Meta:
        db_table = 'tbl_cronograma'
        managed = False