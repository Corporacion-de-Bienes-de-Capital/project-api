from django.db import models
from project.infrastructure.django_models.proyecto import ProyectoORM

class EmpleoORM(models.Model):
    pro = models.OneToOneField(
        ProyectoORM,
        db_column='pro_id',
        on_delete=models.DO_NOTHING,
        primary_key=True,
        related_name='empleo'
    )
    emp_con_nocal = models.IntegerField(null=True, blank=True)
    emp_con_profe = models.IntegerField(null=True, blank=True)
    emp_con_tec = models.IntegerField(null=True, blank=True)
    emp_con_total = models.IntegerField(null=True, blank=True)
    emp_con_nocal_peak = models.IntegerField(null=True, blank=True)
    emp_con_profe_peak = models.IntegerField(null=True, blank=True)
    emp_con_tec_peak = models.IntegerField(null=True, blank=True)
    emp_con_total_peak = models.IntegerField(null=True, blank=True)
    emp_ope_nocal = models.IntegerField(null=True, blank=True)
    emp_ope_profe = models.IntegerField(null=True, blank=True)
    emp_ope_tec = models.IntegerField(null=True, blank=True)
    emp_ope_total = models.IntegerField(null=True, blank=True)
    emp_ope_nocal_peak = models.IntegerField(null=True, blank=True)
    emp_ope_profe_peak = models.IntegerField(null=True, blank=True)
    emp_ope_tec_peak = models.IntegerField(null=True, blank=True)
    emp_ope_total_peak = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_empleo'
        managed = False