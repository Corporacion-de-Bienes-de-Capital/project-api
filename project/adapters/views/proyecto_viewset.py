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
from project.infrastructure.django_models.rel_listado_equipos_descripcion import RelListadoEquiposDescripcionORM
from project.infrastructure.django_models.rel_listado_obras_descripcion import RelListadoObrasDescripcionORM
from project.infrastructure.django_models.productos import ProductosORM
from project.infrastructure.django_models.rel_producto_proyecto import RelProductoProyectoORM
from project.infrastructure.django_models.bitacoras import BitacorasORM
from project.infrastructure.django_models.contacto_proyecto import ContactoProyectoORM
from project.infrastructure.django_models.contactos import ContactosORM
from project.infrastructure.django_models.cronograma import CronogramaORM
from project.infrastructure.django_models.descripcion import DescripcionORM
from project.infrastructure.django_models.empleo import EmpleoORM
from project.infrastructure.django_models.etapas_proyecto import EtapasProyectoORM
from project.infrastructure.django_models.geo import GeoORM
from project.infrastructure.django_models.medio_ambiente import MedioAmbienteORM

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
    
    
    # Recibir, validar y guardar datos de Proyectos enviados por POST

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
        
    # Recibir, validar y guardar datos de proyecto enviados por POST

    def create(self, request):
     try:
        data = request.data
        if not isinstance(data, list):
            data = [data]

        resultados = []

        # --- Mapeo de ForeignKeys ---
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

        # aca recibimos lo que viene en el JSON desde el postman
        for item in data:
            proyecto_data = item.get("tbl_proyecto")
            equipos_data = item.get("rel_listado_equipos_descripcion", [])
            obras_data = item.get("rel_listado_obras_descripcion", [])
            obras_productos = item.get("rel_producto_proyecto", [])
            bitacoras_data = item.get("tbl_bitacoras", [])
            contacto_proyecto_data = item.get("tbl_contacto_proyecto", [])
            contactos_data = item.get("tbl_contactos", [])
            cronogramas_data = item.get("tbl_cronograma", [])
            descripcion_data = item.get("tbl_descripcion", [])
            empleos_data = item.get("tbl_empleo", [])
            etapas_data = item.get("tbl_etapas_proyecto", [])
            geo_data = item.get("tbl_geo", [])
            medio_ambiente_data = item.get("tbl_medio_ambiente", [])


            # si no hay proyecto, devolvemos tal cual con error
            if not proyecto_data:
                item["status"] = "error"
                item["detalle"] = "Falta el objeto tbl_proyecto en el JSON"
                resultados.append(item)
                continue

            try:
                # --- Guardar/actualizar Proyecto ---
                pro_id = proyecto_data.get("pro_id")
                defaults_proyecto = proyecto_data.copy()
                defaults_proyecto.pop("pro_id", None)

                # Convertir FK IDs en instancias
                for campo, modelo in FK_MODEL_MAP.items():
                    if campo in defaults_proyecto:
                        defaults_proyecto[campo] = obtener_instancia_fk(campo, defaults_proyecto[campo])

                proyecto_obj, creado = ProyectoORM.objects.update_or_create(
                    pro_id=pro_id,
                    defaults=defaults_proyecto
                )

                # --- Guardar/actualizar   rel_listado_equipos_descripcion ---
                equipos_resultados = []
                for equipo in equipos_data:
                    lieq_id = equipo.get("lieq_id")
                    defaults_equipo = {
                        "quantity": equipo.get("quantity"),
                        "created_at": equipo.get("created_at"),
                        "edited_at": equipo.get("edited_at"),
                    }

                    equipo_obj, eq_creado = RelListadoEquiposDescripcionORM.objects.update_or_create(
                        lieq_id=lieq_id,
                        pro=proyecto_obj,
                        defaults=defaults_equipo
                    )

                    equipos_resultados.append({
                        "lieq_id": equipo_obj.lieq_id,
                        "pro_id": proyecto_obj.pro_id,
                        "quantity": equipo_obj.quantity,
                        "created_at": equipo_obj.created_at,
                        "edited_at": equipo_obj.edited_at,
                    })

                # --- Guardar/actualizar obras relacionadas ---
                obras_resultados = []
                for obra in obras_data:
                    liob_id = obra.get("liob_id")
                    defaults_obra = {
                        "created_at": obra.get("created_at"),
                        "edited_at": obra.get("edited_at"),
                    }

                    obra_obj, obra_creada = RelListadoObrasDescripcionORM.objects.update_or_create(
                        liob_id=liob_id,
                        pro=proyecto_obj,
                        defaults=defaults_obra
                    )

                    obras_resultados.append({
                        "liob_id": obra_obj.liob_id,
                        "pro_id": proyecto_obj.pro_id,
                        "created_at": obra_obj.created_at,
                        "edited_at": obra_obj.edited_at,
                    })

                # --- Guardar/actualizar productos proyecto relacionados ---
                producto_resultado = []

                for obra in obras_productos:
                    prop_id = obra.get("prop_id")
                    defaults_producto = {
                        "prop_descripcion": obra.get("prop_descripcion"),
                        "prop_cantidad": obra.get("prop_cantidad"),
                        "pro": proyecto_obj,
                        "prod_id": obra.get("prod_id"),
                        "created_at": obra.get("created_at"),
                        "edited_at": obra.get("edited_at"),
                    }

                    producto_obj, obra_creada = RelProductoProyectoORM.objects.update_or_create(
                        prop_id=prop_id,
                        defaults=defaults_producto
                    )

                    producto_resultado.append({
                        "prop_id": producto_obj.prop_id,
                        "pro_id": proyecto_obj.pro_id,
                        "prod_id": producto_obj.prod.prod_id,
                        "prop_descripcion": producto_obj.prop_descripcion,
                        "prop_cantidad": producto_obj.prop_cantidad,
                        "created_at": producto_obj.created_at,
                        "edited_at": producto_obj.edited_at,
                    })

                # --- Guardar/actualizar bitacoras relacionadas ---
                bitacoras_resultado = []

                for bitacora in bitacoras_data:  
                    bita_id = bitacora.get("bita_id")
                    defaults_bitacora = {
                        "bita_inversion": bitacora.get("bita_inversion"),
                        "bita_cronograma": bitacora.get("bita_cronograma"),
                        "bita_estado_sea": bitacora.get("bita_estado_sea"),
                        "bita_otros": bitacora.get("bita_otros"),
                        "pro": proyecto_obj,
                        "is_deleted": bitacora.get("is_deleted"),
                        "created_at": bitacora.get("created_at"),
                        "edited_at": bitacora.get("edited_at"),
                        "user_created_at": bitacora.get("user_created_at"),
                        "user_edited_at": bitacora.get("user_edited_at"),
                    }

                    bitacora_obj, bita_creada = BitacorasORM.objects.update_or_create(
                        bita_id=bita_id,
                        defaults=defaults_bitacora
                    )

                    bitacoras_resultado.append({
                        "bita_id": bitacora_obj.bita_id,
                        "pro_id": proyecto_obj.pro_id,
                        "bita_inversion": bitacora_obj.bita_inversion,
                        "bita_cronograma": bitacora_obj.bita_cronograma,
                        "bita_estado_sea": bitacora_obj.bita_estado_sea,
                        "bita_otros": bitacora_obj.bita_otros,
                        "is_deleted": bitacora_obj.is_deleted,
                        "created_at": bitacora_obj.created_at,
                        "edited_at": bitacora_obj.edited_at,
                        "user_created_at": bitacora_obj.user_created_at,
                        "user_edited_at": bitacora_obj.user_edited_at,
                    })

                # --- Guardar/actualizar contactos_proyecto relacionados ---
                contactos_proyecto_resultado = []

                for contacto in contacto_proyecto_data:  # contactos_data debe ser una lista bajo la clave "rel_contacto_proyecto"
                    copr_id = contacto.get("copr_id")
                    empr_id = contacto.get("empr_id")
                    cont_id = contacto.get("cont_id")
                    pro_id = contacto.get("pro_id")

                    # Instanciar ForeignKeys
                    empresa_obj = obtener_instancia_fk('empresa', empr_id)
                    proyecto_obj = obtener_instancia_fk('proyecto', pro_id)
                    contacto_obj = None
                    if pro_id is not None:
                        try:
                            proyecto_obj = ProyectoORM.objects.get(pk=pro_id)
                        except ProyectoORM.DoesNotExist:
                            proyecto_obj = None
                    if cont_id is not None:
                        try:
                            contacto_obj = ContactosORM.objects.get(pk=cont_id)
                        except ContactosORM.DoesNotExist:
                            contacto_obj = None

                    # Validar que proyecto_obj no sea None antes de crear el objeto
                    if proyecto_obj is None:
                        contacto_resultado = contacto.copy()
                        contacto_resultado["status"] = "error"
                        contacto_resultado["detalle"] = f"No existe ProyectoORM con pro_id={pro_id}"
                        contactos_resultado.append(contacto_resultado)
                        continue

                    defaults_contacto = {
                        "empr": empresa_obj,
                        "cont": contacto_obj,  # ForeignKey a ContactosORM,
                        "copr_tipo": contacto.get("copr_tipo"),
                        "copr_desc": contacto.get("copr_desc"),
                        "pro": proyecto_obj,
                        "created_at": contacto.get("created_at"),
                        "edited_at": contacto.get("edited_at"),
                    }

                    contacto_obj, creado = ContactoProyectoORM.objects.update_or_create(
                        copr_id=copr_id,
                        defaults=defaults_contacto
                    )

                    contactos_proyecto_resultado.append({
                        "copr_id": contacto_obj.copr_id,
                        "empr_id": contacto_obj.empr.empr_id if contacto_obj.empr else None,
                        "cont_id": contacto_obj.cont.cont_id if contacto_obj.cont else None,
                        "copr_tipo": contacto_obj.copr_tipo,
                        "copr_desc": contacto_obj.copr_desc,
                        "pro_id": contacto_obj.pro.pro_id if contacto_obj.pro else None,
                        "created_at": contacto_obj.created_at,
                        "edited_at": contacto_obj.edited_at,
                    })

                
                # Guardar/actualizar contactos relacionados ---
                contactos_resultado = []

                for contacto in contactos_data:  # contactos_data debe ser una lista bajo la clave "rel_contactos"
                    empr_id = contacto.get("empr_id")
                    cont_id = contacto.get("cont_id")
                    contacto_instancia = None
                    if cont_id is not None:
                        try:
                            contacto_instancia = ContactosORM.objects.get(pk=cont_id)
                        except ContactosORM.DoesNotExist:
                            contacto_instancia = None

                    # Instanciar ForeignKey de empresa
                    empresa_obj = None
                    if empr_id is not None:
                        try:
                            empresa_obj = EmpresaORM.objects.get(pk=empr_id)
                        except EmpresaORM.DoesNotExist:
                            empresa_obj = None

                    defaults_contacto = {
                        "cont": contacto_instancia,
                        "cont_nombre": contacto.get("cont_nombre"),
                        "cont_telefono": contacto.get("cont_telefono"),
                        "cont_correo": contacto.get("cont_correo"),
                        "area_id": contacto.get("area_id"),
                        "carc_id": contacto.get("carc_id"),
                        "empr": empresa_obj,
                        "cont_es_interno": contacto.get("cont_es_interno"),
                        "carc_descripcion": contacto.get("carc_descripcion"),
                        "cont_observacion": contacto.get("cont_observacion"),
                        "is_deleted": contacto.get("is_deleted"),
                        "created_at": contacto.get("created_at"),
                        "edited_at": contacto.get("edited_at"),
                        "deleted_at": contacto.get("deleted_at"),
                    }

                    contacto_obj, creado = ContactosORM.objects.update_or_create(
                        copr_id=contacto.get("copr_id"),
                        defaults=defaults_contacto
                    )

                    contactos_resultado.append({
                        "cont_id": contacto_obj.cont_id,
                        "empr_id": contacto_obj.empr.empr_id if contacto_obj.empr else None,
                        "cont_nombre": contacto_obj.cont_nombre,
                        "cont_telefono": contacto_obj.cont_telefono,
                        "cont_correo": contacto_obj.cont_correo,
                        "area_id": contacto_obj.area_id,
                        "carc_id": contacto_obj.carc_id,
                        "cont_es_interno": contacto_obj.cont_es_interno,
                        "carc_descripcion": contacto_obj.carc_descripcion,
                        "cont_observacion": contacto_obj.cont_observacion,
                        "is_deleted": contacto_obj.is_deleted,
                        "created_at": contacto_obj.created_at,
                        "edited_at": contacto_obj.edited_at,
                        "deleted_at": contacto_obj.deleted_at,
                    })

                # Guardar/actualizar cronogramas relacionados
                cronogramas_resultado = []

                for cronograma in cronogramas_data:  # cronogramas_data debe ser una lista bajo la clave "tbl_cronograma"
                    cron_id = cronograma.get("cron_id")
                    cont_id = cronograma.get("cont_id")
                    pro_id = cronograma.get("pro_id")

                    # Instanciar ForeignKeys
                    contacto_obj = None
                    if cont_id is not None:
                        try:
                            contacto_obj = ContactosORM.objects.get(pk=cont_id)
                        except ContactosORM.DoesNotExist:
                            contacto_obj = None

                    proyecto_obj = None
                    if pro_id is not None:
                        try:
                            proyecto_obj = ProyectoORM.objects.get(pk=pro_id)
                        except ProyectoORM.DoesNotExist:
                            proyecto_obj = None

                    defaults_cronograma = {
                        "cont": contacto_obj,
                        "tiob_id": cronograma.get("tiob_id"),
                        "cron_obs": cronograma.get("cron_obs"),
                        "cron_etapa": cronograma.get("cron_etapa"),
                        "pro": proyecto_obj,
                        "created_at": cronograma.get("created_at"),
                        "edited_at": cronograma.get("edited_at"),
                    }

                    cronograma_obj, creado = CronogramaORM.objects.update_or_create(
                        cron_id=cron_id,
                        defaults=defaults_cronograma
                    )

                    cronogramas_resultado.append({
                        "cron_id": cronograma_obj.cron_id,
                        "cont_id": cronograma_obj.cont.cont_id if cronograma_obj.cont else None,
                        "tiob_id": cronograma_obj.tiob_id,
                        "cron_obs": cronograma_obj.cron_obs,
                        "cron_etapa": cronograma_obj.cron_etapa,
                        "pro_id": cronograma_obj.pro.pro_id if cronograma_obj.pro else None,
                        "created_at": cronograma_obj.created_at,
                        "edited_at": cronograma_obj.edited_at,
                    })

                # Guardar/actualizar descripciones relacionadas
                descripciones_resultado = []
                if isinstance(descripcion_data, dict):
                    descripcion_data = [descripcion_data] # Asegura que descripcion_data sea una lista de diccionarios
                elif not isinstance(descripcion_data, list):
                    descripcion_data = []

                for descripcion in descripcion_data:
                    
                    
                    desc_id = descripcion.get("desc_id")
                    pro_id = descripcion.get("pro_id")

                    # Instanciar ForeignKey de proyecto
                    proyecto_obj = None
                    if pro_id is not None:
                        try:
                            proyecto_obj = ProyectoORM.objects.get(pk=pro_id)
                        except ProyectoORM.DoesNotExist:
                            proyecto_obj = None

                    defaults_descripcion = {
                        "desc_objetivo": descripcion.get("desc_objetivo"),
                        "desc_resumen": descripcion.get("desc_resumen"),
                        "pro": proyecto_obj,
                        "is_deleted": descripcion.get("is_deleted"),
                        "created_at": descripcion.get("created_at"),
                        "edited_at": descripcion.get("edited_at"),
                        "desc_ubicacion": descripcion.get("desc_ubicacion"),
                        "desc_vidautil": descripcion.get("desc_vidautil"),
                        "desc_obras": descripcion.get("desc_obras"),
                    }

                    descripcion_obj, creada = DescripcionORM.objects.update_or_create(
                        desc_id=desc_id,
                        defaults=defaults_descripcion
                    )

                    descripciones_resultado.append({
                        "desc_id": descripcion_obj.desc_id,
                        "desc_objetivo": descripcion_obj.desc_objetivo,
                        "desc_resumen": descripcion_obj.desc_resumen,
                        "pro_id": descripcion_obj.pro.pro_id if descripcion_obj.pro else None,
                        "is_deleted": descripcion_obj.is_deleted,
                        "created_at": descripcion_obj.created_at,
                        "edited_at": descripcion_obj.edited_at,
                        "desc_ubicacion": descripcion_obj.desc_ubicacion,
                        "desc_vidautil": descripcion_obj.desc_vidautil,
                        "desc_obras": descripcion_obj.desc_obras,
                    })
                

                # Guardar/actualizar empleos relacionados
                empleos_resultado = []             
                if isinstance(empleos_data, dict): # Asegura que empleos_data sea una lista de diccionarios
                    empleos_data = [empleos_data]
                elif not isinstance(empleos_data, list):
                    empleos_data = []

                for empleo in empleos_data:
                    if not isinstance(empleo, dict):
                        continue  # Salta elementos que no sean dict
                    pro_id = empleo.get("pro_id")

                    # Instanciar ForeignKey de proyecto
                    proyecto_obj = None
                    if pro_id is not None:
                        try:
                            proyecto_obj = ProyectoORM.objects.get(pk=pro_id)
                        except ProyectoORM.DoesNotExist:
                            proyecto_obj = None

                    defaults_empleo = {
                        "emp_con_nocal": empleo.get("emp_con_nocal"),
                        "emp_con_profe": empleo.get("emp_con_profe"),
                        "emp_con_tec": empleo.get("emp_con_tec"),
                        "emp_con_total": empleo.get("emp_con_total"),
                        "emp_con_nocal_peak": empleo.get("emp_con_nocal_peak"),
                        "emp_con_profe_peak": empleo.get("emp_con_profe_peak"),
                        "emp_con_tec_peak": empleo.get("emp_con_tec_peak"),
                        "emp_con_total_peak": empleo.get("emp_con_total_peak"),
                        "emp_ope_nocal": empleo.get("emp_ope_nocal"),
                        "emp_ope_profe": empleo.get("emp_ope_profe"),
                        "emp_ope_tec": empleo.get("emp_ope_tec"),
                        "emp_ope_total": empleo.get("emp_ope_total"),
                        "emp_ope_nocal_peak": empleo.get("emp_ope_nocal_peak"),
                        "emp_ope_profe_peak": empleo.get("emp_ope_profe_peak"),
                        "emp_ope_tec_peak": empleo.get("emp_ope_tec_peak"),
                        "emp_ope_total_peak": empleo.get("emp_ope_total_peak"),
                    }

                    empleo_obj, creado = EmpleoORM.objects.update_or_create(
                        pro=proyecto_obj,
                        defaults=defaults_empleo
                    )

                    empleos_resultado.append({
                        "pro_id": empleo_obj.pro.pro_id if empleo_obj.pro else None,
                        "emp_con_nocal": empleo_obj.emp_con_nocal,
                        "emp_con_profe": empleo_obj.emp_con_profe,
                        "emp_con_tec": empleo_obj.emp_con_tec,
                        "emp_con_total": empleo_obj.emp_con_total,
                        "emp_con_nocal_peak": empleo_obj.emp_con_nocal_peak,
                        "emp_con_profe_peak": empleo_obj.emp_con_profe_peak,
                        "emp_con_tec_peak": empleo_obj.emp_con_tec_peak,
                        "emp_con_total_peak": empleo_obj.emp_con_total_peak,
                        "emp_ope_nocal": empleo_obj.emp_ope_nocal,
                        "emp_ope_profe": empleo_obj.emp_ope_profe,
                        "emp_ope_tec": empleo_obj.emp_ope_tec,
                        "emp_ope_total": empleo_obj.emp_ope_total,
                        "emp_ope_nocal_peak": empleo_obj.emp_ope_nocal_peak,
                        "emp_ope_profe_peak": empleo_obj.emp_ope_profe_peak,
                        "emp_ope_tec_peak": empleo_obj.emp_ope_tec_peak,
                        "emp_ope_total_peak": empleo_obj.emp_ope_total_peak,
                    })


                # Guardar/actualizar etapas_proyecto relacionadas               
                etapas_resultado = []

                # Normalización robusta
                if isinstance(etapas_data, dict):
                    etapas_data = [etapas_data]
                elif not isinstance(etapas_data, list):
                    etapas_data = []

                for etapa in etapas_data:
                    if not isinstance(etapa, dict):
                        continue
                    pro_id = etapa.get("pro_id")
                    proyecto_obj = None
                    if pro_id is not None:
                        try:
                            proyecto_obj = ProyectoORM.objects.get(pk=pro_id)
                        except ProyectoORM.DoesNotExist:
                            proyecto_obj = None

                    defaults_etapa = {
                        "ing_conc_inicio": etapa.get("ing_conc_inicio"),
                        "ing_conc_fin": etapa.get("ing_conc_fin"),
                        "ing_basica_inicio": etapa.get("ing_basica_inicio"),
                        "ing_basica_fin": etapa.get("ing_basica_fin"),
                        "ing_detalle_inicio": etapa.get("ing_detalle_inicio"),
                        "ing_detalle_fin": etapa.get("ing_detalle_fin"),
                        "cons_inicio": etapa.get("cons_inicio"),
                        "cons_fin": etapa.get("cons_fin"),
                    }

                    etapa_obj, creado = EtapasProyectoORM.objects.update_or_create(
                        pro=proyecto_obj,
                        defaults=defaults_etapa
                    )

                    etapas_resultado.append({
                        "pro_id": etapa_obj.pro.pro_id if etapa_obj.pro else None,
                        "ing_conc_inicio": etapa_obj.ing_conc_inicio,
                        "ing_conc_fin": etapa_obj.ing_conc_fin,
                        "ing_basica_inicio": etapa_obj.ing_basica_inicio,
                        "ing_basica_fin": etapa_obj.ing_basica_fin,
                        "ing_detalle_inicio": etapa_obj.ing_detalle_inicio,
                        "ing_detalle_fin": etapa_obj.ing_detalle_fin,
                        "cons_inicio": etapa_obj.cons_inicio,
                        "cons_fin": etapa_obj.cons_fin,
                    })

                # --- Guardar/actualizar geo relacionados ---
                geo_resultado = []
                # Normalización robusta
                if isinstance(geo_data, dict):
                    geo_data = [geo_data] # Asegura que geo_data sea una lista de diccionarios
                elif not isinstance(geo_data, list):
                    geo_data = []

                for geo in geo_data:
                    if not isinstance(geo, dict):
                        continue
                    pro_id = geo.get("pro_id")
                    proyecto_obj = None
                    if pro_id is not None:
                        try:
                            proyecto_obj = ProyectoORM.objects.get(pk=pro_id)
                        except ProyectoORM.DoesNotExist:
                            proyecto_obj = None

                    defaults_geo = {
                        "latitud": geo.get("latitud"),
                        "longitud": geo.get("longitud"),
                        "created_at": geo.get("created_at"),
                        "edited_at": geo.get("edited_at"),
                    }

                    geo_obj, creado = GeoORM.objects.update_or_create(
                        pro=proyecto_obj,
                        defaults=defaults_geo
                    )

                    geo_resultado.append({
                        "pro_id": geo_obj.pro.pro_id if geo_obj.pro else None,
                        "latitud": geo_obj.latitud,
                        "longitud": geo_obj.longitud,
                        "created_at": geo_obj.created_at,
                        "edited_at": geo_obj.edited_at,
                    })

                # --- Guardar/actualizar medio_ambiente relacionados ---
                medio_ambiente_resultado = []
                # Normalización robusta
                if isinstance(medio_ambiente_data, dict):
                    medio_ambiente_data = [medio_ambiente_data]  # Asegura que medio_ambiente_data sea una lista de diccionarios
                elif not isinstance(medio_ambiente_data, list):
                    medio_ambiente_data = []

                for mamb in medio_ambiente_data:
                    if not isinstance(mamb, dict):
                        continue
                    mamb_id = mamb.get("mamb_id")
                    pro_id = mamb.get("pro_id")
                    proyecto_obj = None
                    if pro_id is not None:
                        try:
                            proyecto_obj = ProyectoORM.objects.get(pk=pro_id)
                        except ProyectoORM.DoesNotExist:
                            proyecto_obj = None

                    defaults_mamb = {
                        "mamb_emp_pres_proyecto": mamb.get("mamb_emp_pres_proyecto"),
                        "mamb_tipo_proyecto": mamb.get("mamb_tipo_proyecto"),
                        "mamb_fecha_presentacion": mamb.get("mamb_fecha_presentacion"),
                        "mamb_contacto": mamb.get("mamb_contacto"),
                        "mamb_plazo_evaluacion": mamb.get("mamb_plazo_evaluacion"),
                        "mamb_dias_legales": mamb.get("mamb_dias_legales"),
                        "mamb_dias_totales": mamb.get("mamb_dias_totales"),
                        "esea_id": mamb.get("esea_id"),
                        "ppro_id": mamb.get("ppro_id"),
                        "pro": proyecto_obj,
                        "mamb_enlace_sea": mamb.get("mamb_enlace_sea"),
                        "is_history": mamb.get("is_history"),
                        "is_deleted": mamb.get("is_deleted"),
                        "mamb_fecha_calificacion": mamb.get("mamb_fecha_calificacion"),
                        "mamb_descripcion": mamb.get("mamb_descripcion"),
                    }

                    mamb_obj, creado = MedioAmbienteORM.objects.update_or_create(
                        mamb_id=mamb_id,
                        defaults=defaults_mamb
                    )

                    medio_ambiente_resultado.append({
                        "mamb_id": mamb_obj.mamb_id,
                        "pro_id": mamb_obj.pro.pro_id if mamb_obj.pro else None,
                        "mamb_emp_pres_proyecto": mamb_obj.mamb_emp_pres_proyecto,
                        "mamb_tipo_proyecto": mamb_obj.mamb_tipo_proyecto,
                        "mamb_fecha_presentacion": mamb_obj.mamb_fecha_presentacion,
                        "mamb_contacto": mamb_obj.mamb_contacto,
                        "mamb_plazo_evaluacion": mamb_obj.mamb_plazo_evaluacion,
                        "mamb_dias_legales": mamb_obj.mamb_dias_legales,
                        "mamb_dias_totales": mamb_obj.mamb_dias_totales,
                        "esea_id": mamb_obj.esea_id,
                        "ppro_id": mamb_obj.ppro_id,
                        "mamb_enlace_sea": mamb_obj.mamb_enlace_sea,
                        "is_history": mamb_obj.is_history,
                        "is_deleted": mamb_obj.is_deleted,
                        "mamb_fecha_calificacion": mamb_obj.mamb_fecha_calificacion,
                        "mamb_descripcion": mamb_obj.mamb_descripcion,
                    })

                # reconstruye el objeto en el mismo formato que enviaste desde post y lo devuelve  igual.
                item["tbl_proyecto"] = proyecto_data
                item["rel_listado_equipos_descripcion"] = equipos_resultados
                item["rel_listado_obras_descripcion"] = obras_resultados
                item["rel_producto_proyecto"] = producto_resultado
                item["tbl_bitacoras"] = bitacoras_resultado
                item["tbl_contacto_proyecto"] = contactos_proyecto_resultado
                item["tbl_cronograma"] = cronogramas_resultado
                item["tbl_descripcion"] = descripciones_resultado
                item["tbl_empleo"] = empleos_resultado
                item["tbl_etapas_proyecto"] = etapas_resultado
                
                item["status"] = "creado" if creado else "actualizado"

            except Exception as inner_e:
                item["status"] = "error"
                item["detalle"] = f"Error al guardar: {str(inner_e)}"

            resultados.append(item)

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