from rest_framework import serializers
from .empresa_serializer import EmpresaSerializer
from project.infrastructure.django_models.proyecto import ProyectoORM



class ProyectoSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField(required=False)
    pro_nombre = serializers.CharField(required=False)
    empresa = EmpresaSerializer(required=False)
    
    
    def to_representation(self, instance):
        pro_id = getattr(instance, 'pro_id', None) or getattr(instance, 'id', None)
        pro_nombre = getattr(instance, 'pro_nombre', None) or getattr(instance, 'nombre', None)
        empresa_obj = getattr(instance, 'empresa', None)


        data = {
            'pro_id': pro_id,
            'pro_nombre': pro_nombre,
        }

        # Empresa (empr_id y empr_nombre)
        if empresa_obj:
            empr_id = getattr(empresa_obj, 'empr_id', None) or getattr(empresa_obj, 'id', None)
            empr_nombre = getattr(empresa_obj, 'empr_nombre', None) or getattr(empresa_obj, 'nombre', None)
            data['empresa'] = {
                'empr_id': empr_id,
                'empr_nombre': empr_nombre
            }
        else:
            data['empresa'] = None

        # Estado SEA (trae los campos esea_id y esea_nombre desde MedioAmbienteORM relacionado)
        from project.infrastructure.django_models.medio_ambiente import MedioAmbienteORM
        medio_ambiente_obj = MedioAmbienteORM.objects.filter(pro_id=instance).first()
        if medio_ambiente_obj and medio_ambiente_obj.esea:
            data['esea_id'] = medio_ambiente_obj.esea.esea_id
            data['esea_nombre'] = medio_ambiente_obj.esea.esea_nombre
        else:
            data['esea_id'] = None
            data['esea_nombre'] = None

        return data


        
class ProyectoORMSerializer(serializers.ModelSerializer):

    tinv_nombre = serializers.CharField(source='tinv_id.tinv_nombre', read_only=True)
    tinv_id = serializers.IntegerField(source='tinv_id.tinv_id', read_only=True)
    seco_nombre = serializers.CharField(source='seco_id.seco_nombre', read_only=True)
    seco_id = serializers.IntegerField(source='seco_id.seco_id', read_only=True)
    tplo_nombre = serializers.CharField(source='tplo_id.tplo_nombre', read_only=True)
    tplo_id = serializers.IntegerField(source='tplo_id.tplo_id', read_only=True)
    tpro_nombre = serializers.CharField(source='tpro_id.tpro_nombre', read_only=True)
    tpro_id = serializers.IntegerField(source='tpro_id.tpro_id', read_only=True)   
    dist_nombre = serializers.CharField(source='dist_id.dist_nombre', read_only=True)
    dist_id = serializers.IntegerField(source='dist_id.dist_id', read_only=True)    
    relacion_hidrogeno_nombre = serializers.CharField(source='relacion_hidrogeno_id.relacion_hidrogeno_nombre', read_only=True)
    relacion_hidrogeno_id = serializers.IntegerField(source='relacion_hidrogeno_id.relacion_hidrogeno_id', read_only=True) 
    estatus_cont_nombre = serializers.CharField(source='estatus_cont_id.estatus_cont_nombre', read_only=True)
    estatus_cont_id = serializers.IntegerField(source='estatus_cont_id.estatus_cont_id', read_only=True)
    pais_nombre = serializers.CharField(source='pais_id.pais_nombre', read_only=True)
    pais_id = serializers.IntegerField(source='pais_id.pais_id', read_only=True)
    reg_nombre = serializers.CharField(source='reg_id.reg_nombre', read_only=True)
    reg_id = serializers.IntegerField(source='reg_id.reg_id', read_only=True)
    prov_nombre = serializers.CharField(source='prov_id.prov_nombre', read_only=True)
    prov_id = serializers.IntegerField(source='prov_id.prov_id', read_only=True)
    comu_nombre = serializers.CharField(source='comu_id.comu_nombre', read_only=True)
    comu_id = serializers.IntegerField(source='comu_id.comu_id', read_only=True)
    empresa_nombre = serializers.CharField(source='empresa.empr_nombre', read_only=True)

    #Campos relacionados a Estado SEA desde MedioAmbienteORM
    esea_id = serializers.SerializerMethodField()
    esea_nombre = serializers.SerializerMethodField()
    def get_esea_id(self, obj):
        medio_ambiente_obj = obj.medioambiente.first()
        return medio_ambiente_obj.esea.esea_id if medio_ambiente_obj and medio_ambiente_obj.esea else None
    def get_esea_nombre(self, obj):
        medio_ambiente_obj = obj.medioambiente.first()
        return medio_ambiente_obj.esea.esea_nombre if medio_ambiente_obj and medio_ambiente_obj.esea else None


    class Meta:
        model = ProyectoORM
        fields = [
            'pro_id', 'pro_nombre',
            'empresa', 'empresa_nombre',
            'pais_id', 'pais_nombre',
            'reg_id', 'reg_nombre',
            'prov_id', 'prov_nombre',
            'comu_id', 'comu_nombre',
            'pro_ubicacion',
            'pro_producto',
            'pro_capacidad_produccion',
            'pro_monto_inversion',
            'pro_descripcion',
            'pro_cron_fecha',
            'pro_diferido',
            'tinv_id', 'tinv_nombre',
            'seco_id', 'seco_nombre',
            'tplo_id', 'tplo_nombre',
            'tpro_id', 'tpro_nombre',
            'dist_id', 'dist_nombre',
            'estatus_cont_id', 'estatus_cont_nombre',
            'region_incidencia_proyecto',
            'relacion_hidrogeno_id', 'relacion_hidrogeno_nombre',
            'is_covid_affected',
            'is_green_hydrogen',
            'is_deleted',
            'created_at',
            'edited_at',
            'user_created_at',
            'user_edited_at', 
            'confidencial',
            'mindha',
            'sea_afectado',
            'desaladora',  
            'codigo_bip',
            'codigo_sea',
            'esea_id',
            'esea_nombre',

        ]  # Personalizar la lista, solo algunos campos o todos
            #fields = '__all__'  # Todos los campos del modelo

    
class ProyectoListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProyectoORM  # Al modelo que corresponda
        fields = ['pro_id', 'pro_nombre']

