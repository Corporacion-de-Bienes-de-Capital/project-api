from rest_framework.test import APITestCase
from django.urls import reverse


class ProyectoEquipoErrorTest(APITestCase):
    def test_equipo_sin_proyecto(self):
        url = reverse('proyecto-list')
        data = {
            "rel_listado_equipos_descripcion": [
                {"lieq_id": 1, "quantity": 5}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['resultado'][0]['status'], 'error')
        self.assertIn('Falta el objeto tbl_proyecto', response.data['resultado'][0]['detalle'])


#Probar endpoint de listar proyectos
from rest_framework.test import APITestCase
from django.urls import reverse

# class ProyectoListTest(APITestCase):
#     def test_listar_proyectos(self):
#         url = reverse('proyecto-list')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertIsInstance(response.data, list)
#         self.assertGreaterEqual(len(response.data), 1)
#         self.assertIn('pro_nombre', response.data[0])


# #Para correr los tests en PowerShell
# $env:DJANGO_SETTINGS_MODULE="proapi.settings"; pytest


#Probar endpoint de listar proyectos
from rest_framework.test import APITestCase
from django.urls import reverse

class ProyectoListTest(APITestCase):
    def test_listar_proyectos(self):
        url = reverse('proyecto-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn('pro_nombre', response.data[0])