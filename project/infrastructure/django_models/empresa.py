from django.db import models

class EmpresaORM(models.Model):
    nombre = models.CharField(max_length=200)

    class Meta:
        db_table = 'tbl_empresa'
