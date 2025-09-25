from rest_framework import viewsets, status
from rest_framework.response import Response
from project.infrastructure.repository.empresa_repository_impl import EmpresaRepositoryImpl
from project.domain.services.empresa_service import EmpresaService
from project.api.serializers.empresa_serializer import EmpresaSerializer
from rest_framework.decorators import action
from project.infrastructure.django_models.proyecto import ProyectoORM
from project.infrastructure.django_models.empresa import EmpresaORM
from project.api.serializers.proyectoserializer import ProyectoSerializer

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
    
    def get_view_name(self):
        action = getattr(self, 'action', None)
        # Cambia el nombre de la opción en Extra Actions según la acción
        if action == 'empresas_sin_proyectos':
            if self.request and self.request.path.endswith('/sin-proyectos/'):
                return "Empresas sin proyecto"
            return "Empresas sin proyecto"
        if action == 'empresas_con_proyectos':
            return "Empresas con proyecto"
        return "Lista de Empresas"
    
       
    #Recibir, validar y guardar datos enviados por POST
    def create(self, request):
        empresas = request.data
        if not isinstance(empresas, list):
            return Response({"error": "Se esperaba una lista de empresas"}, status=400)

        resultados = []
        for empresa in empresas:
            empr_id = empresa.get('empr_id')
            empr_nombre = empresa.get('empr_nombre')
            empr_rut = empresa.get('empr_rut')
            if not (empr_id and empr_nombre and empr_rut):
                empresa_resultado = empresa.copy()
                empresa_resultado["status"] = "error"
                empresa_resultado["detalle"] = "Faltan campos obligatorios"
                resultados.append(empresa_resultado)
                continue
            # Aquí puedes crear o actualizar la empresa en la BD
                # obj, creado = EmpresaORM.objects.update_or_create(
                #     empr_id=empr_id,
                #     defaults={"empr_nombre": empr_nombre, "empr_rut": empr_rut}
                # )
                # if creado
                #     resultados.append({"empr_id": empr_id, "status": "creado"})
                # else:
                #     resultados.append({"empr_id": empr_id, "status": "actualizado"})

                # Por ahora, solo simula el resultado:

            empresa_resultado = empresa.copy()
            empresa_resultado["status"] = "procesado"
            resultados.append(empresa_resultado)

        return Response({"resultado": resultados}, status=201)
    
        #Lista todos los proyectos asociados a una empresa específica.
    # URL CON PARAMETRO: http://127.0.0.1:8000/api/proyectos/por-empresa/?empresa_id=44765
    queryset = ProyectoORM.objects.filter(is_deleted=0)
    serializer_class = ProyectoSerializer

    # @action(
    #     detail=False, methods=['get'], url_path='por-empresa', name='Listar proyectos por empresa')
    # def listar_por_empresa(self, request):
    #     #Endpoint para listar proyectos de una empresa.
    #     #El usuario debe pasar el parámetro ?empresa_id=ID en la URL.
    #     """
    #     Proyectos que solo estan en desarollo
        
    #     Ejemplo: /api/proyectos/por-empresa/?empresa_id=1
    #     """
    #     empresa_id = request.query_params.get('empresa_id')
    #     if not empresa_id:
    #         return Response({'error': 'Debe proporcionar el parámetro empresa_id.'}, status=status.HTTP_400_BAD_REQUEST)
    #     proyectos = ProyectoORM.objects.filter(empresa_id=empresa_id, is_deleted=0)
    #     serializer = ProyectoSerializer(proyectos, many=True)
    #     return Response(serializer.data)
    @action(detail=False, methods=['get'], url_path='con-proyectos')
    def empresas_con_proyectos(self, request):
        empresas = EmpresaORM.objects.filter(proyectos__isnull=False).distinct()
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sin-proyectos')
    def empresas_sin_proyectos(self, request):
        empresas = EmpresaORM.objects.filter(proyectos__isnull=True)
        serializer = EmpresaSerializer(empresas, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=['get'], url_path='proyectos')
    def proyectos_por_empresa(self, request, pk=None):
        """
        Devuelve solo el nombre de la empresa y una lista de nombres de proyectos asociados.
        Ejemplo: /empresas/13/proyectos/
        """
        try:
            empresa = EmpresaORM.objects.get(empr_id=pk)
        except EmpresaORM.DoesNotExist:
            return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        proyectos = ProyectoORM.objects.filter(empresa_id=pk, is_deleted=0)
        lista_proyectos = [
            {'pro_id': p.pro_id, 'pro_nombre': p.pro_nombre}
            for p in proyectos
        ]
        data = {
            'empr_nombre': empresa.empr_nombre,
            'proyectos': lista_proyectos
        }
        return Response(data)
    
    