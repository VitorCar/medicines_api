from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from manufacturers.models import Manufacturers
from manufacturers.serializers import ManufacturersSerializer


class ManufacturersViewsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        content_type = ContentType.objects.get_for_model(Manufacturers)
        permissions = Permission.objects.filter(content_type=content_type)
        self.user.user_permissions.set(permissions)

        self.manufacturer = Manufacturers.objects.create(
            name='Test Manufacturer',
            Address='123 Test St',
            contact_details='test@example.com'
        )

    def test_list_manufacturers(self):
        response = self.client.get('/api/v1/manufacturers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Manufacturer')

    def test_create_manufacturer(self):
        data = {
            'name': 'New Manufacturer',
            'Address': '456 New St',
            'contact_details': 'new@example.com'
        }
        response = self.client.post('/api/v1/manufacturers/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Manufacturers.objects.count(), 2)
        self.assertEqual(response.data['name'], 'New Manufacturer')

    def test_retrieve_manufacturer(self):
        response = self.client.get(f'/api/v1/manufacturers/{self.manufacturer.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Manufacturer')

    def test_update_manufacturer_put(self):
        data = {
            'name': 'Updated Manufacturer',
            'Address': '789 Updated St',
            'contact_details': 'updated@example.com'
        }
        response = self.client.put(f'/api/v1/manufacturers/{self.manufacturer.pk}/', data)
        self.assertEqual(response.status_code, 200)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, 'Updated Manufacturer')

    def test_update_manufacturer_patch(self):
        data = {'name': 'Patched Manufacturer'}
        response = self.client.patch(f'/api/v1/manufacturers/{self.manufacturer.pk}/', data)
        self.assertEqual(response.status_code, 200)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, 'Patched Manufacturer')

    def test_delete_manufacturer(self):
        response = self.client.delete(f'/api/v1/manufacturers/{self.manufacturer.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Manufacturers.objects.count(), 0)

    def test_serializer_valid(self):
        data = {
            'name': 'Valid Manufacturer',
            'Address': 'Valid Address',
            'contact_details': 'valid@example.com'
        }
        serializer = ManufacturersSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid(self):
        data = {'name': ''}
        serializer = ManufacturersSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)


class ManufacturersPermissionsTestCase(APITestCase):

    def setUp(self):
        self.user_no_perms = User.objects.create_user(username='no_perms', password='testpass')
        self.user_view = User.objects.create_user(username='view_user', password='testpass')

        content_type = ContentType.objects.get_for_model(Manufacturers)
        view_perm = Permission.objects.get(content_type=content_type, codename='view_manufacturers')
        self.user_view.user_permissions.add(view_perm)

        self.manufacturer = Manufacturers.objects.create(
            name='Test Manufacturer',
            Address='123 Test St',
            contact_details='test@example.com'
        )

    def test_list_unauthenticated(self):
        response = self.client.get('/api/v1/manufacturers/')
        self.assertEqual(response.status_code, 401)

    def test_list_no_permissions(self):
        self.client.force_authenticate(user=self.user_no_perms)
        response = self.client.get('/api/v1/manufacturers/')
        self.assertEqual(response.status_code, 403)

    def test_list_with_view_permission(self):
        self.client.force_authenticate(user=self.user_view)
        response = self.client.get('/api/v1/manufacturers/')
        self.assertEqual(response.status_code, 200)

    def test_create_no_permissions(self):
        self.client.force_authenticate(user=self.user_view)
        data = {
            'name': 'New Manufacturer',
            'Address': '456 New St',
            'contact_details': 'new@example.com'
        }
        response = self.client.post('/api/v1/manufacturers/', data)
        self.assertEqual(response.status_code, 403)
