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
        return "Lista de Empresas"
    
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
        lista_proyectos = [p.pro_nombre for p in proyectos]
        data = {
            'empr_nombre': empresa.empr_nombre,
            'proyectos': lista_proyectos
        }
        return Response(data)
    
    