from rest_framework import serializers
from .empresa_serializer import EmpresaSerializer
from project.infrastructure.django_models.proyecto import ProyectoORM

class ProyectoSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField(required=False)
    pro_nombre = serializers.CharField(required=False)
    empresa = EmpresaSerializer(required=False)
    
    
    def to_representation(self, instance):
        pro_id = getattr(instance, 'pro_id', None) or getattr(instance, 'id', None)
        pro_nombre = getattr(instance, 'pro_nombre', None) or getattr(instance, 'nombre', None)
        empresa_obj = getattr(instance, 'empresa', None)
        
        data = {
            'pro_id': pro_id,
            'pro_nombre': pro_nombre,
        }

        # Obtener el estado del proyecto
        # Asegurarse de que pro_estado es un objeto relacionado y no un ID
        estado_nombre = getattr(getattr(instance, 'pro_estado', None), 'estado_nombre', None)
        data['pro_estado'] = getattr(instance, 'pro_estado_id', None)  # el id del estado
        data['estado_nombre'] = estado_nombre  # el nombre del estado

        if empresa_obj:
            # Buscar id y nombre de la empresa, usando ambos posibles nombres
            empr_id = getattr(empresa_obj, 'empr_id', None) or getattr(empresa_obj, 'id', None)
            empr_nombre = getattr(empresa_obj, 'empr_nombre', None) or getattr(empresa_obj, 'nombre', None)
            data['empresa'] = {
                'empr_id': empr_id,
                'empr_nombre': empr_nombre
            }
        else:
            data['empresa'] = None

        return data
class ProyectoORMSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProyectoORM
        fields = '__all__'