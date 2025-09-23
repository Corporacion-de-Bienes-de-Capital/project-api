from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.text import slugify

from project.domain.services.empresa_service import EmpresaService
from project.domain.services.proyecto_service import ProyectoService

from project.api.serializers.proyectoserializer import ProyectoSerializer
from project.api.serializers.empresa_serializer import EmpresaSerializer
from project.api.serializers.proyectoserializer import ProyectoORMSerializer
from project.api.serializers.proyectoserializer import ProyectoListaSerializer

from project.infrastructure.django_models.proyecto import ProyectoORM
from project.infrastructure.django_models.sector_economico import SectorEconomicoORM

from project.infrastructure.repository.empresa_repository_impl import EmpresaRepositoryImpl
from project.infrastructure.repository.proyecto_repository_impl import ProyectoRepositoryImpl

from project.infrastructure.cosmosdb_service import log_event

import pytz




    
class ProyectoViewSet(viewsets.ViewSet):
    def get_view_name(self):
        return "Lista de Proyectos"
    

    def list(self, request):
        log_event(
            user=request.user,
            endpoint=request.path,
            method=request.method,
            extra={"query_params": dict(request.query_params)}
        )
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
    
    
    # @action(detail=True, methods=['get'], url_path='estado')
    # def estado(self, request, pk=None):
    #     try:
    #         proyecto = ProyectoORM.objects.get(pk=pk)
    #     except ProyectoORM.DoesNotExist:
    #         return Response({'error': 'Proyecto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = ProyectoSerializer(proyecto)
    #     return Response(serializer.data)
    

    #Listar proyectos por sector económico usando slug
    @action(detail=False, methods=['get'], url_path='sector-economico/(?P<parametro>[^/.]+)')
    def listar_por_sector_economico(self, request, parametro=None):
        
    # Registrar el evento en CosmosDB
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip:
            ip = ip.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR", None)

        extra = {
            "user_pk": getattr(request.user, "pk", None),
            "username": getattr(request.user, "username", str(request.user)),
            "ip": ip,
            "query_params": dict(request.query_params),
            "body": request.data if hasattr(request, "data") else None
        }
        log_event(
            user=request.user,
            endpoint=request.path,
            method=request.method,
            extra=extra
        )
        
        """
        Endpoint para listar proyectos filtrados por el slug del sector económico.
        """
        try:
            # Transformar el slug si es necesario (por ejemplo, convertir a minúsculas)
            slug_ = slugify(parametro)

            sector = next(
                (s for s in SectorEconomicoORM.objects.all() if slugify(s.seco_nombre) == slug_), None
            )

            # Filtrar proyectos relacionados con el sector económico
            if sector:
                proyectos = ProyectoORM.objects.filter(seco_id=sector.seco_id)


            # Serializar los proyectos
            serializer = ProyectoListaSerializer(proyectos, many=True)

            # Retornar la respuesta
            return Response(serializer.data)
        except SectorEconomicoORM.DoesNotExist:
            return Response({'error': 'Sector económico no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            # Manejo de errores generales
            #return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) para depurar
            return Response({'error': 'Sector económico no encontrado'}, status=status.HTTP_404_NOT_FOUND)