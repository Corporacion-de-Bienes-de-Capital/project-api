from django.db import models
from .empresa import EmpresaORM

class ProyectoORM(models.Model):
    nombre = models.CharField(max_length=200)
    empresa = models.ForeignKey(EmpresaORM, on_delete=models.DO_NOTHING, related_name='proyectos', null=True, blank=True)

    class Meta:
        db_table = 'tbl_proyecto'
