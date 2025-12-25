from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from routes_of_administration.models import RoutesOfAdministration
from routes_of_administration.serializers import RoutesOfAdministrationSerializer


class RoutesOfAdministrationViewsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        content_type = ContentType.objects.get_for_model(RoutesOfAdministration)
        permissions = Permission.objects.filter(content_type=content_type)
        self.user.user_permissions.set(permissions)

        self.route = RoutesOfAdministration.objects.create(
            name='Oral',
            type='ENT',
            description='Via oral'
        )

    def test_list_routes_of_administration(self):
        response = self.client.get('/api/v1/administration/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Oral')

    def test_create_route_of_administration(self):
        data = {
            'name': 'Intravenosa',
            'type': 'PAR',
            'description': 'Via intravenosa'
        }
        response = self.client.post('/api/v1/administration/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(RoutesOfAdministration.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Intravenosa')

    def test_retrieve_route_of_administration(self):
        response = self.client.get(f'/api/v1/administration/{self.route.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Oral')

    def test_update_route_of_administration_put(self):
        data = {
            'name': 'Oral Updated',
            'type': 'ENT',
            'description': 'Via oral atualizada'
        }
        response = self.client.put(f'/api/v1/administration/{self.route.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.route.refresh_from_db()
        self.assertEqual(self.route.name, 'Oral Updated')

    def test_update_route_of_administration_patch(self):
        data = {'name': 'Oral Patched'}
        response = self.client.patch(f'/api/v1/administration/{self.route.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.route.refresh_from_db()
        self.assertEqual(self.route.name, 'Oral Patched')

    def test_delete_route_of_administration(self):
        response = self.client.delete(f'/api/v1/administration/{self.route.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(RoutesOfAdministration.objects.count(), 0)

    def test_serializer_valid(self):
        data = {
            'name': 'Tópica',
            'type': 'TOP',
            'description': 'Via tópica'
        }
        serializer = RoutesOfAdministrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid(self):
        data = {'name': '', 'type': 'INVALID'}
        serializer = RoutesOfAdministrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('type', serializer.errors)
