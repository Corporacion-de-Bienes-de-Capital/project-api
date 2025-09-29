from django.db import models
from project.infrastructure.django_models.proyecto import ProyectoORM
from project.infrastructure.django_models.productos import ProductosORM


class RelProductoProyectoORM(models.Model):
    prop_id = models.AutoField(primary_key=True)
    prop_descripcion = models.CharField(max_length=150, null=True, blank=True)
    prop_cantidad = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    pro = models.ForeignKey(
        ProyectoORM,
        db_column='pro_id',
        on_delete=models.DO_NOTHING,
        related_name='productos_proyecto'
    )
    prod = models.ForeignKey(
        ProductosORM,
        db_column='prod_id',
        on_delete=models.DO_NOTHING,
        related_name='proyectos_producto'
    )

    class Meta:
        db_table = 'rel_producto_proyecto'
        managed = False  # Solo si la tabla ya existe y no quieres que Django la maneje
        indexes = [
            models.Index(fields=['pro'], name='fk_pro_id'),
            models.Index(fields=['prod'], name='fk_prod_id'),
        ]

    def __str__(self):
        return f"{self.prop_descripcion} - Proyecto {self.pro.pro_id}"
