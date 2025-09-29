from django.db import models
from project.infrastructure.django_models.proyecto import ProyectoORM
from project.infrastructure.django_models.empresa import EmpresaORM
from project.infrastructure.django_models.contactos import ContactosORM

class ContactoProyectoORM(models.Model):
    copr_id = models.AutoField(primary_key=True)
    
    copr_tipo = models.IntegerField(null=True, blank=True)
    copr_desc = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.BigIntegerField(null=True, blank=True)
    edited_at = models.BigIntegerField(null=True, blank=True)

    cont = models.ForeignKey(
        ContactosORM,
        db_column='cont_id',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name='contacto_proyectos'
    )

    empr = models.ForeignKey(
        EmpresaORM,
        db_column='empr_id',
        on_delete=models.DO_NOTHING, 
        related_name='contacto_proyectos' 
        )
    
    pro = models.ForeignKey(
        ProyectoORM,
        db_column='pro_id', on_delete=models.DO_NOTHING,
        related_name='contacto_proyectos' 
        )

    class Meta:
        db_table = 'tbl_contacto_proyecto'
        managed = False