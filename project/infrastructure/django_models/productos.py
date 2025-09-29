from django.db import models


class ProductosORM(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_nombre = models.CharField(max_length=150, null=True, blank=True)
    prod_unidad_medida = models.CharField(max_length=150, null=True, blank=True)
    is_deleted = models.BooleanField(null=True, blank=True)  # tinyint(1) -> BooleanField
    created_at = models.IntegerField(null=True, blank=True)
    edited_at = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_productos'
        managed = False  # Cambiar a True si quieres que Django maneje la tabla

    def __str__(self):
        return self.prod_nombre or f"Productos {self.prod_id}"
