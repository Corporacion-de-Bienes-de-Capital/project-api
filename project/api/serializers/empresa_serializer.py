
from rest_framework import serializers

class EmpresaSerializer(serializers.Serializer):
    empr_id = serializers.IntegerField(required=False)
    empr_nombre = serializers.CharField(required=False)
    empr_rut = serializers.CharField(required=False)

    def to_representation(self, instance):
        empr_id = getattr(instance, 'empr_id', None) or getattr(instance, 'id', None)
        empr_nombre = getattr(instance, 'empr_nombre', None) or getattr(instance, 'nombre', None)
        empr_rut = getattr(instance, 'empr_rut', None) or getattr(instance, 'rut', None)
        return {
            'empr_id': empr_id,
            'empr_nombre': empr_nombre,
            'empr_rut': empr_rut
        }
