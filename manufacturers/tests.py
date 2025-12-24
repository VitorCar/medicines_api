from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from manufacturers.models import Manufacturers
from manufacturers.serializers import ManufacturersSerializer


class ManufacturersViewsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        # Assign permissions
        content_type = ContentType.objects.get_for_model(Manufacturers)
        permissions = Permission.objects.filter(content_type=content_type)
        self.user.user_permissions.set(permissions)

        self.manufacturer = Manufacturers.objects.create(
            name='Test Manufacturer',
            Address='Test Address',
            contact_details='Test Contact'
        )

    def test_list_manufacturers(self):
        response = self.client.get('/api/v1/manufacturers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Manufacturer')

    def test_create_manufacturer(self):
        data = {
            'name': 'New Manufacturer',
            'Address': 'New Address',
            'contact_details': 'New Contact'
        }
        response = self.client.post('/api/v1/manufacturers/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Manufacturers.objects.count(), 2)
        self.assertEqual(response.data['name'], 'New Manufacturer')

    def test_retrieve_manufacturer(self):
        response = self.client.get(f'/api/v1/manufacturers/{self.manufacturer.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Manufacturer')

    def test_update_manufacturer(self):
        data = {
            'name': 'Updated Manufacturer',
            'Address': 'Updated Address',
            'contact_details': 'Updated Contact'
        }
        response = self.client.put(f'/api/v1/manufacturers/{self.manufacturer.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, 'Updated Manufacturer')

    def test_partial_update_manufacturer(self):
        data = {'name': 'Partially Updated Manufacturer'}
        response = self.client.patch(f'/api/v1/manufacturers/{self.manufacturer.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, 'Partially Updated Manufacturer')

    def test_delete_manufacturer(self):
        response = self.client.delete(f'/api/v1/manufacturers/{self.manufacturer.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Manufacturers.objects.count(), 0)

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/manufacturers/')
        self.assertEqual(response.status_code, 401)

    def test_insufficient_permissions(self):
        # Remove permissions
        self.user.user_permissions.clear()
        response = self.client.get('/api/v1/manufacturers/')
        self.assertEqual(response.status_code, 403)