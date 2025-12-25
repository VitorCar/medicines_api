from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from pharmaceutical_forms.models import PharmaceuticalForms
from pharmaceutical_forms.serializers import PharmaceuticalFormsSerializer


class PharmaceuticalFormsViewsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        content_type = ContentType.objects.get_for_model(PharmaceuticalForms)
        Permissions = Permission.objects.filter(content_type=content_type)
        self.user.user_permissions.set(Permissions)

        self.pharmaceutical = PharmaceuticalForms.objects.create(
            name='Test pharmaceutical',
            category='LIQ',
            description='Test pharmaceutical forms'
        )

    def test_list_pharmaceutical_forms(self):
        response = self.client.get('/api/v1/pharmaceutical/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test pharmaceutical')

    def test_create_pharmaceutical_forms(self):
        data = {
            'name':'Test pharmaceutical',
            'category':'SOL',
            'description':'Test pharmaceutical forms'
        }
        response = self.client.post('/api/v1/pharmaceutical/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PharmaceuticalForms.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Test pharmaceutical')

    def test_retrieve_pharmaceutical_forms(self):
        response = self.client.get(f'/api/v1/pharmaceutical/{self.pharmaceutical.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test pharmaceutical')

    def test_update_pharmaceutical_forms_put(self):
        data = {
            'name': 'Updated pharmaceutical',
            'category': 'SOL',
            'description': 'Updated description'
        }
        response = self.client.put(f'/api/v1/pharmaceutical/{self.pharmaceutical.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.pharmaceutical.refresh_from_db()
        self.assertEqual(self.pharmaceutical.name, 'Updated pharmaceutical')

    def test_update_pharmaceutical_forms_patch(self):
        data = {'name': 'Patched pharmaceutical'}
        response = self.client.patch(f'/api/v1/pharmaceutical/{self.pharmaceutical.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.pharmaceutical.refresh_from_db()
        self.assertEqual(self.pharmaceutical.name, 'Patched pharmaceutical')

    def test_delete_pharmaceutical_forms(self):
        response = self.client.delete(f'/api/v1/pharmaceutical/{self.pharmaceutical.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(PharmaceuticalForms.objects.count(), 0)

    def test_serializer_valid(self):
        data = {
            'name': 'Valid pharmaceutical',
            'category': 'LIQ',
            'description': 'Valid description'
        }
        serializer = PharmaceuticalFormsSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid(self):
        data = {'name': '', 'category': 'INVALID'}
        serializer = PharmaceuticalFormsSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('category', serializer.errors)
