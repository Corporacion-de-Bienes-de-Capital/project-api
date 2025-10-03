from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


#Pruebas para endpoint publico de empresas
class EmpresaAPITest(APITestCase):
    def test_listar_empresas(self):
        url = reverse('empresa-list')  # Ajusta el nombre según tus rutas
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertIn('empr_nombre', response.data[0])

    def test_obtener_empresa_por_id(self):
        url = reverse('empresa-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['empr_id'], 1)
        self.assertIn('empr_nombre', response.data)


# #Prueba de autenticación para endpoint de empresas
# class EmpresaAuthAPITest(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.token = Token.objects.create(user=self.user)

#     def test_listar_empresas_autenticado(self):
#         url = reverse('empresa-list')
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)


