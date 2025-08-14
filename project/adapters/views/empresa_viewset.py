from rest_framework import viewsets, status
from rest_framework.response import Response
from project.infrastructure.repository.empresa_repository_impl import EmpresaRepositoryImpl
from project.domain.services.empresa_service import EmpresaService
from project.api.serializers.empresa_serializer import EmpresaSerializer
from rest_framework.decorators import action

class EmpresaViewSet(viewsets.ViewSet):
    # sólo endpoints de lectura
    def list(self, request):
        repo = EmpresaRepositoryImpl()
        servicio = EmpresaService(repo)
        empresas = servicio.listar_empresas()
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        repo = EmpresaRepositoryImpl()
        servicio = EmpresaService(repo)
        empresa = servicio.obtener(int(pk))
        if empresa is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data)