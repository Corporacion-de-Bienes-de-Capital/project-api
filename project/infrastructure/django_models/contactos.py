from django.db import models
from project.infrastructure.django_models.empresa import EmpresaORM
from project.infrastructure.django_models.proyecto import ProyectoORM
# Si tienes modelos para Area y Cargo, puedes importarlos y usar ForeignKey

class ContactosORM(models.Model):
    cont_id = models.AutoField(primary_key=True)
    cont_nombre = models.CharField(max_length=150, null=True, blank=True)
    cont_telefono = models.CharField(max_length=150, null=True, blank=True)
    cont_correo = models.CharField(max_length=150, null=True, blank=True)
    area_id = models.IntegerField(null=True, blank=True)  # Cambia a ForeignKey si tienes modelo AreaORM
    carc_id = models.IntegerField(null=True, blank=True)  # Cambia a ForeignKey si tienes modelo CargoORM
    cont_es_interno = models.BooleanField(null=True, blank=True)
    carc_descripcion = models.CharField(max_length=100, null=True, blank=True)
    cont_observacion = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(null=True, blank=True)
    created_at = models.IntegerField(null=True, blank=True)
    edited_at = models.IntegerField(null=True, blank=True)
    deleted_at = models.IntegerField(null=True, blank=True)

    empr = models.ForeignKey(
        EmpresaORM,
        db_column='empr_id',
        on_delete=models.DO_NOTHING,
        related_name='contactos'
    )

    class Meta:
        db_table = 'tbl_contactos'
        managed = False
        unique_together = (('cont_id', 'empr'),)