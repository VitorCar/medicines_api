from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from drug_identification.models import DrugIdentification
from drug_identification.serializers import DrugIdentificationSerializer, DrugIdentificationListSerializer
from manufacturers.models import Manufacturers
from pharmaceutical_forms.models import PharmaceuticalForms
from routes_of_administration.models import RoutesOfAdministration


class DrugIdentificationViewsTestCase(APITestCase):

    def setUp(self):
        # Usuário autenticado
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

        # Permissões do model DrugIdentification
        content_type = ContentType.objects.get_for_model(DrugIdentification)
        permissions = Permission.objects.filter(content_type=content_type)
        self.user.user_permissions.set(permissions)

        # Objetos relacionados
        self.manufacturer = Manufacturers.objects.create(
            name='Test Manufacturer',
            Address='Test Address',
            contact_details='Test Contact'
        )
        self.pharm_form = PharmaceuticalForms.objects.create(
            name='Comprimido',
            description='Forma farmacêutica sólida'
        )
        self.route = RoutesOfAdministration.objects.create(
            name='Oral',
            type='ENT',
            description='Via oral'
        )

        # Objeto base
        self.drug = DrugIdentification.objects.create(
            trade_name='Aspirina',
            generic_name='Ácido Acetilsalicílico',
            type_of_medicine='GEN',
            presentation='Caixa com 30 comprimidos',
            active_ingredient='Ácido Acetilsalicílico 100mg',
            storage_care='Manter em local fresco',
            medical_prescription='SIM',
            doping_alert='NAO',
            estimated_value='R$ 10,00'
        )
        self.drug.pharmaceutical_form.add(self.pharm_form)
        self.drug.routes_of_administration.add(self.route)
        self.drug.manufacturers.add(self.manufacturer)

        # URLs (reverse)
        self.list_url = reverse('drug-creat-list')
        self.detail_url = reverse(
            'drug-detail-view',
            args=[self.drug.id]
        )
        self.stats_url = reverse('drug-stats-view')

    # -------------------------
    # LIST
    # -------------------------
    def test_list_drug_identifications(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['trade_name'], 'Aspirina')

    # -------------------------
    # CREATE
    # -------------------------
    def test_create_drug_identification(self):
        data = {
            'trade_name': 'Paracetamol',
            'generic_name': 'Paracetamol',
            'type_of_medicine': 'GEN',
            'pharmaceutical_form': [self.pharm_form.id],
            'routes_of_administration': [self.route.id],
            'presentation': 'Caixa com 20 comprimidos',
            'active_ingredient': 'Paracetamol 500mg',
            'storage_care': 'Manter em local seco',
            'medical_prescription': 'NAO',
            'doping_alert': 'NAO',
            'manufacturers': [self.manufacturer.id],
            'estimated_value': 'R$ 5,00'
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DrugIdentification.objects.count(), 2)
        self.assertEqual(response.data['trade_name'], 'Paracetamol')

    def test_create_drug_identification_invalid(self):
        data = {'trade_name': ''}

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -------------------------
    # RETRIEVE
    # -------------------------
    def test_retrieve_drug_identification(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['trade_name'], 'Aspirina')

    # -------------------------
    # UPDATE
    # -------------------------
    def test_update_drug_identification_put(self):
        data = {
            'trade_name': 'Aspirina Updated',
            'generic_name': 'Ácido Acetilsalicílico',
            'type_of_medicine': 'GEN',
            'pharmaceutical_form': [self.pharm_form.id],
            'routes_of_administration': [self.route.id],
            'presentation': 'Caixa com 30 comprimidos',
            'active_ingredient': 'Ácido Acetilsalicílico 100mg',
            'storage_care': 'Manter em local fresco',
            'medical_prescription': 'SIM',
            'doping_alert': 'NAO',
            'manufacturers': [self.manufacturer.id],
            'estimated_value': 'R$ 10,00'
        }

        response = self.client.put(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.drug.refresh_from_db()
        self.assertEqual(self.drug.trade_name, 'Aspirina Updated')

    def test_update_drug_identification_patch(self):
        data = {'trade_name': 'Aspirina Patched'}

        response = self.client.patch(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.drug.refresh_from_db()
        self.assertEqual(self.drug.trade_name, 'Aspirina Patched')

    # -------------------------
    # DELETE
    # -------------------------
    def test_delete_drug_identification(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DrugIdentification.objects.count(), 0)

    # -------------------------
    # STATS
    # -------------------------
    def test_drug_identification_stats(self):
        response = self.client.get(self.stats_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_drug', response.data)
        self.assertEqual(response.data['total_drug'], 1)

    # -------------------------
    # AUTH / PERMISSION
    # -------------------------
    def test_list_drug_identifications_unauthenticated(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # -------------------------
    # SERIALIZER
    # -------------------------
    def test_serializer_valid(self):
        data = {
            'trade_name': 'Ibuprofeno',
            'generic_name': 'Ibuprofeno',
            'type_of_medicine': 'GEN',
            'pharmaceutical_form': [self.pharm_form.id],
            'routes_of_administration': [self.route.id],
            'presentation': 'Caixa com 10 comprimidos',
            'active_ingredient': 'Ibuprofeno 400mg',
            'storage_care': 'Manter em local fresco',
            'medical_prescription': 'NAO',
            'doping_alert': 'NAO',
            'manufacturers': [self.manufacturer.id],
            'estimated_value': 'R$ 15,00'
        }

        serializer = DrugIdentificationSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid(self):
        data = {'trade_name': ''}

        serializer = DrugIdentificationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('trade_name', serializer.errors)
