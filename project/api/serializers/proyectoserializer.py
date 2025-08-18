from rest_framework import serializers
from .empresa_serializer import EmpresaSerializer

class ProyectoSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField(required=False)
    pro_nombre = serializers.CharField(required=False)
    empresa = EmpresaSerializer(required=False)

    def to_representation(self, instance):
        """
        Personaliza la representación para incluir datos de la empresa relacionados,
        simulando el resultado del JOIN de tu consulta SQL.
        """
        # Intenta obtener los atributos de ambas posibles fuentes
        pro_id = getattr(instance, 'pro_id', None) or getattr(instance, 'id', None)
        pro_nombre = getattr(instance, 'pro_nombre', None) or getattr(instance, 'nombre', None)
        empresa_obj = getattr(instance, 'empresa', None)

        data = {
            'pro_id': pro_id,
            'pro_nombre': pro_nombre,
        }

        if empresa_obj:
            data['empresa'] = {
                'empr_id': getattr(empresa_obj, 'empr_id', None),
                'empr_nombre': getattr(empresa_obj, 'empr_nombre', None)
            }
            data['empr_id'] = getattr(empresa_obj, 'empr_id', None)
        else:
            data['empresa'] = None
            data['empr_id'] = None

        return data