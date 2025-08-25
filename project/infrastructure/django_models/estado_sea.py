from django.db import models

class EstadoSeaORM(models.Model):
	esea_id = models.AutoField(primary_key=True)
	esea_nombre = models.CharField(max_length=150, null=True, blank=True)
	pais_id = models.IntegerField(null=True, blank=True)
	esea_is_deleted = models.PositiveSmallIntegerField(null=True, blank=True)

	class Meta:
		db_table = 'tbl_estado_sea'
		managed = False
