from rest_framework import viewsets, status
from rest_framework.response import Response
from project.infrastructure.repository.proyecto_repository_impl import ProyectoRepositoryImpl
from project.domain.services.proyecto_service import ProyectoService
from project.api.serializers.proyectoserializer import ProyectoSerializer
from rest_framework.decorators import action

class ProyectoViewSet(viewsets.ViewSet):
    # sólo endpoints de lectura
    def list(self, request):
        repo = ProyectoRepositoryImpl()
        servicio = ProyectoService(repo)
        proyectos = servicio.listar_proyectos_con_empresas()
        serializer = ProyectoSerializer(proyectos, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        repo = ProyectoRepositoryImpl()
        servicio = ProyectoService(repo)
        proyecto = servicio.obtener(int(pk))
        if proyecto is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProyectoSerializer(proyecto)
        return Response(serializer.data)