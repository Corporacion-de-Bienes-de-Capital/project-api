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
from project.infrastructure.django_models.proyecto import ProyectoORM
from project.infrastructure.django_models.empresa import EmpresaORM
from project.infrastructure.django_models.estado_pro import EstadoProyectoORM
from project.infrastructure.django_models.tipo_inversion import TipoInversionORM
from project.infrastructure.django_models.sector_economico import SectorEconomicoORM
from project.infrastructure.django_models.tipologias import TipologiasORM
from project.infrastructure.django_models.tipo_proyecto import TipoProyectoORM
from project.infrastructure.django_models.generacion_distribuida import GeneracionDistribuidaORM
from project.infrastructure.django_models.relacion_hidrogeno import RelacionHidrogenoORM
from project.infrastructure.django_models.estatus_contingencia import EstatusContingenciaORM
from project.infrastructure.django_models.pais import PaisORM
from project.infrastructure.django_models.region import RegionORM
from project.infrastructure.django_models.provincias import ProvinciasORM
from project.infrastructure.django_models.comunas import ComunasORM


from project.infrastructure.repository.empresa_repository_impl import EmpresaRepositoryImpl
from project.infrastructure.repository.proyecto_repository_impl import ProyectoRepositoryImpl

from project.infrastructure.cosmosdb_service import log_event
import pytz




    
class ProyectoViewSet(viewsets.ViewSet):
    def get_view_name(self):
        return "Lista de Proyectos"
    

    def list(self, request):
        # Inicio Registrar el Log en CosmosDB
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
        #Cierrar Registrar el log en CosmosDB
        
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
    
    
    #Recibir, validar y guardar datos enviados por POST

    def create(self, request):
        # Mapeo de campos ForeignKey a sus modelos
        FK_MODEL_MAP = {
            'pro_estado': EstadoProyectoORM,
            'empresa': EmpresaORM,
            'tinv_id': TipoInversionORM,
            'seco_id': SectorEconomicoORM,
            'tplo_id': TipologiasORM,
            'tpro_id': TipoProyectoORM,
            'dist_id': GeneracionDistribuidaORM,
            'relacion_hidrogeno_id': RelacionHidrogenoORM,
            'estatus_cont_id': EstatusContingenciaORM,
            'pais_id': PaisORM,
            'reg_id': RegionORM,
            'prov_id': ProvinciasORM,
            'comu_id': ComunasORM,
        }

        def obtener_instancia_fk(campo, valor):
            modelo = FK_MODEL_MAP.get(campo)
            if modelo and valor not in [None, '', 0]:
                try:
                    return modelo.objects.get(pk=valor)
                except modelo.DoesNotExist:
                    return None
            return None

        try:
            proyectos = request.data  #Recibir base de proyectos JSON
            if not isinstance(proyectos, list):
                proyectos = [proyectos]

            resultados = []
            campos_requeridos = [
                "pro_id", "pro_nombre", "pro_producto", "pro_capacidad_produccion", "pro_ubicacion",
                "region_incidencia_proyecto", "pro_monto_inversion", "pro_descripcion", "is_covid_affected",
                "is_green_hydrogen", "relacion_hidrogeno_id", "is_deleted", "created_at", "edited_at",
                "user_created_at", "user_edited_at", "comu_id", "pro_cron_fecha", "pro_diferido",
                "confidencial", "mindha", "sea_afectado", "desaladora", "codigo_bip", "codigo_sea",
                "pro_estado", "empr_id", "tinv_id", "seco_id", "tplo_id", "tpro_id", "dist_id",
                "estatus_cont_id", "pais_id", "reg_id", "prov_id"
            ]
            for proyecto in proyectos:
                # Validar que todos los campos estén presentes
                if not all(campo in proyecto for campo in campos_requeridos):
                    proyecto_resultado = proyecto.copy()
                    proyecto_resultado["status"] = "error"
                    proyecto_resultado["detalle"] = "Faltan campos obligatorios"
                    resultados.append(proyecto_resultado)
                    continue

                pro_id = proyecto.get('pro_id')
                defaults = {
                    "pro_nombre": proyecto.get('pro_nombre'),
                    "pro_producto": proyecto.get('pro_producto'),
                    "pro_capacidad_produccion": proyecto.get('pro_capacidad_produccion'),
                    "pro_ubicacion": proyecto.get('pro_ubicacion'),
                    "region_incidencia_proyecto": proyecto.get('region_incidencia_proyecto'),
                    "pro_monto_inversion": proyecto.get('pro_monto_inversion'),
                    "pro_descripcion": proyecto.get('pro_descripcion'),
                    "is_covid_affected": proyecto.get('is_covid_affected'),
                    "is_green_hydrogen": proyecto.get('is_green_hydrogen'),
                    "relacion_hidrogeno_id": obtener_instancia_fk('relacion_hidrogeno_id', proyecto.get('relacion_hidrogeno_id')),
                    "is_deleted": proyecto.get('is_deleted'),
                    "created_at": proyecto.get('created_at'),
                    "edited_at": proyecto.get('edited_at'),
                    "user_created_at": proyecto.get('user_created_at'),
                    "user_edited_at": proyecto.get('user_edited_at'),
                    "comu_id": obtener_instancia_fk('comu_id', proyecto.get('comu_id')),
                    "pro_cron_fecha": proyecto.get('pro_cron_fecha'),
                    "pro_diferido": proyecto.get('pro_diferido'),
                    "confidencial": proyecto.get('confidencial'),
                    "mindha": proyecto.get('mindha'),
                    "sea_afectado": proyecto.get('sea_afectado'),
                    "desaladora": proyecto.get('desaladora'),
                    "codigo_bip": proyecto.get('codigo_bip'),
                    "codigo_sea": proyecto.get('codigo_sea'),
                    "pro_estado": obtener_instancia_fk('pro_estado', proyecto.get('pro_estado')),
                    "empresa": obtener_instancia_fk('empresa', proyecto.get('empr_id')),
                    "tinv_id": obtener_instancia_fk('tinv_id', proyecto.get('tinv_id')),
                    "seco_id": obtener_instancia_fk('seco_id', proyecto.get('seco_id')),
                    "tplo_id": obtener_instancia_fk('tplo_id', proyecto.get('tplo_id')),
                    "tpro_id": obtener_instancia_fk('tpro_id', proyecto.get('tpro_id')),
                    "dist_id": obtener_instancia_fk('dist_id', proyecto.get('dist_id')),
                    "estatus_cont_id": obtener_instancia_fk('estatus_cont_id', proyecto.get('estatus_cont_id')),
                    "pais_id": obtener_instancia_fk('pais_id', proyecto.get('pais_id')),
                    "reg_id": obtener_instancia_fk('reg_id', proyecto.get('reg_id')),
                    "prov_id": obtener_instancia_fk('prov_id', proyecto.get('prov_id')),
                }

                obj, creado = ProyectoORM.objects.update_or_create(
                    pro_id=pro_id,
                    defaults=defaults
                )
                proyecto_resultado = proyecto.copy()
                proyecto_resultado["status"] = "creado" if creado else "actualizado"
                resultados.append(proyecto_resultado)

            return Response({"resultado": resultados}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    


    
    
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
        
    # Registrar el Log en CosmosDB
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
    #Cerrar Registrar el log en CosmosDB    
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