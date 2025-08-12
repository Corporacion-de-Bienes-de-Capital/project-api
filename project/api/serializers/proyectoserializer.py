from rest_framework import serializers
from .empresa_serializer import EmpresaSerializer

class ProyectoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    empresa = EmpresaSerializer(allow_null=True)
