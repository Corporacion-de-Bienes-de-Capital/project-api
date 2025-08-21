from rest_framework import viewsets, status
from rest_framework.response import Response
from project.infrastructure.repository.proyecto_repository_impl import ProyectoRepositoryImpl
from project.domain.services.proyecto_service import ProyectoService
from project.api.serializers.proyectoserializer import ProyectoSerializer
from project.infrastructure.repository.empresa_repository_impl import EmpresaRepositoryImpl
from project.domain.services.empresa_service import EmpresaService
from project.api.serializers.empresa_serializer import EmpresaSerializer
from project.infrastructure.django_models.proyecto import ProyectoORM
from project.api.serializers.proyectoserializer import ProyectoORMSerializer
from project.api.serializers.proyectoserializer import ProyectoListaSerializer
from rest_framework.decorators import action

class EmpresaViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repo = EmpresaRepositoryImpl()
        self.servicio = EmpresaService(self.repo)
    
    def list(self, request):
        empresas = self.servicio.listar_empresas()
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        empresa = self.servicio.obtener(int(pk))
        if empresa is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data)
    
class ProyectoViewSet(viewsets.ViewSet):
    def get_view_name(self):
        return "Lista de Proyectos"
    def list(self, request):
        repo = ProyectoRepositoryImpl()
        servicio = ProyectoService(repo)
        proyectos = servicio.listar_proyectos_con_empresas()
        serializer = ProyectoListaSerializer(proyectos, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            proyecto = ProyectoORM.objects.get(pk=pk)
        except ProyectoORM.DoesNotExist:
            return Response({'error': 'Proyecto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProyectoORMSerializer(proyecto)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['get'], url_path='estado')
    def estado(self, request, pk=None):
        try:
            proyecto = ProyectoORM.objects.get(pk=pk)
        except ProyectoORM.DoesNotExist:
            return Response({'error': 'Proyecto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProyectoSerializer(proyecto)
        return Response(serializer.data)