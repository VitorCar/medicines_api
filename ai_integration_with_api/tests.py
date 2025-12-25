from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch, MagicMock

from rest_framework import status
from rest_framework.test import APITestCase


class AIIntegrationViewsTestCase(APITestCase):

    def setUp(self):
        # Usuário autenticado
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

        # URLs (reverse)
        self.pharmacy_url = reverse('ai-pharmacy')
        self.leaflet_url = reverse('ai-leaflet')

    # -------------------------
    # SEARCH PHARMACY
    # -------------------------
    @patch('ai_integration_with_api.views.client.models.generate_content')
    def test_search_pharmacy_success(self, mock_generate):
        mock_response = MagicMock()
        mock_response.text = '[{"nome": "Farmácia A", "endereco": "Rua X", "cep": "12345"}]'
        mock_generate.return_value = mock_response

        data = {'city': 'São Paulo', 'state': 'SP'}
        response = self.client.post(self.pharmacy_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('suggestions_ia', response.data)
        self.assertEqual(len(response.data['suggestions_ia']), 1)

    def test_search_pharmacy_missing_data(self):
        data = {'city': 'São Paulo'}
        response = self.client.post(self.pharmacy_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('erro', response.data)

    @patch('ai_integration_with_api.views.client.models.generate_content')
    def test_search_pharmacy_json_error(self, mock_generate):
        mock_generate.side_effect = Exception("API Error")

        data = {'city': 'São Paulo', 'state': 'SP'}
        response = self.client.post(self.pharmacy_url, data)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('erro', response.data)

    # -------------------------
    # MEDICINE LEAFLET
    # -------------------------
    @patch('ai_integration_with_api.views.client.models.generate_content')
    def test_medicine_leaflet_success(self, mock_generate):
        mock_response = MagicMock()
        mock_response.text = '{"nome": "Aspirina", "composicao_resumida": "Ácido", "indicacao_principal": "Dor", "posologia_adulto": "1 comprimido", "contraindicacao_chave": "Alergia"}'
        mock_generate.return_value = mock_response

        data = {'remedy': 'Aspirina'}
        response = self.client.post(self.leaflet_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('suggestions_ia', response.data)
        self.assertEqual(response.data['suggestions_ia']['nome'], 'Aspirina')

    def test_medicine_leaflet_missing_data(self):
        data = {}
        response = self.client.post(self.leaflet_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('erro', response.data)

    @patch('ai_integration_with_api.views.client.models.generate_content')
    def test_medicine_leaflet_json_error(self, mock_generate):
        mock_generate.side_effect = Exception("API Error")

        data = {'remedy': 'Aspirina'}
        response = self.client.post(self.leaflet_url, data)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('erro', response.data)

    # -------------------------
    # AUTH / PERMISSION
    # -------------------------
    def test_search_pharmacy_unauthenticated(self):
        self.client.force_authenticate(user=None)

        data = {'city': 'São Paulo', 'state': 'SP'}
        response = self.client.post(self.pharmacy_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_medicine_leaflet_unauthenticated(self):
        self.client.force_authenticate(user=None)

        data = {'remedy': 'Aspirina'}
        response = self.client.post(self.leaflet_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
