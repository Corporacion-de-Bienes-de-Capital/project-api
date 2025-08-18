
from django.contrib import admin

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from project.adapters.views.proyecto_viewset import ProyectoViewSet
from project.adapters.views.empresa_viewset import EmpresaViewSet

class CustomRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        view = super().get_api_root_view(api_urls)
        view.cls.__name__ = "Información de Empresas y Proyectos de CBC"
        view.cls.get_view_name = lambda self: "Información de Empresas y Proyectos de CBC"
        return view

router = CustomRouter()
router.register(r'proyectos', ProyectoViewSet, basename='proyecto')
router.register(r'empresas', EmpresaViewSet, basename='empresa')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
