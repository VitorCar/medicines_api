from django.db.models import Count
from rest_framework import generics, views, response, status
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermissions
from drug_identification.models import DrugIdentification
from drug_identification.serializers import DrugIdentificationSerializer, DrugIdentificationListSerializer
from manufacturers.models import Manufacturers
from pharmaceutical_forms.models import PharmaceuticalForms
from routes_of_administration.models import RoutesOfAdministration


class DrugIdentificationListCreateAPIView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = DrugIdentification.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DrugIdentificationListSerializer
        return DrugIdentificationSerializer


class DrugIdentificationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = DrugIdentification.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DrugIdentificationListSerializer
        return DrugIdentificationSerializer


class DrugIdentificationStatsView(views.APIView):
    permission_classes = (IsAuthenticated,)
    queryset = DrugIdentification.objects.all()

    def get(self, request):
        total_drug = self.queryset.count()
        total_pharmaceutical_form = PharmaceuticalForms.objects.count()
        total_routes_of_administration = RoutesOfAdministration.objects.count()
        drug_by_routes_of_administration = self.queryset.values('routes_of_administration__name').annotate(count=Count('id'))
        total_types_of_medicine = self.queryset.values('type_of_medicine').annotate(count=Count('id'))
        drug_by_manufacturers = self.queryset.values('manufacturers__name').annotate(count=Count('id'))
        total_manufacturers = Manufacturers.objects.count()
        total_medical_prescription = self.queryset.values('medical_prescription').annotate(count=Count('trade_name'))
        total_doping_alert = self.queryset.values('doping_alert').annotate(count=Count('trade_name'))

        return response.Response(
            data={
                'total_drug': total_drug,
                'total_types_of_medicine': total_types_of_medicine,
                'total_pharmaceutical_form': total_pharmaceutical_form,
                'total_routes_of_administration': total_routes_of_administration,
                'drug_by_routes_of_administration': drug_by_routes_of_administration,
                'drug_by_manufacturers': drug_by_manufacturers,
                'total_manufacturers': total_manufacturers,
                'total_medical_prescription': total_medical_prescription,
                'total_doping_alert': total_doping_alert,
            }, status=status.HTTP_200_OK
        )
