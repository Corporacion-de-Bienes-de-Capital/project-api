from django.db import models
from project.infrastructure.django_models.pais import PaisORM

class RegionORM(models.Model):
	reg_id = models.AutoField(primary_key=True)
	reg_nombre = models.CharField(max_length=150, null=True, blank=True)
	reg_codigo = models.CharField(max_length=150, null=True, blank=True)
	reg_representacion = models.CharField(max_length=20, null=True, blank=True)
	is_deleted = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	created_at = models.PositiveIntegerField(null=True, blank=True)
	edited_at = models.PositiveIntegerField(null=True, blank=True)
	
    # Relacion con pais
	pais_id = models.ForeignKey(
		PaisORM,
		on_delete=models.DO_NOTHING,
		db_column='pais_id',
		null=False,
		blank=False
	)
      
      
	class Meta:
            db_table = 'tbl_region'
            managed = False

    
