from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermissions
from pharmaceutical_forms.models import PharmaceuticalForms
from pharmaceutical_forms.serializers import PharmaceuticalFormsSerializer


class PharmaceuticalFormsListCreateApiView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = PharmaceuticalForms.objects.all()
    serializer_class = PharmaceuticalFormsSerializer


class PharmaceuticalFormsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = PharmaceuticalForms.objects.all()
    serializer_class = PharmaceuticalFormsSerializer
