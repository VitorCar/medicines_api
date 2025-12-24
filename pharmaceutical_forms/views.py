from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from app.permissions import GlobalDefaultPermissions
from pharmaceutical_forms.models import PharmaceuticalForms
from pharmaceutical_forms.serializers import PharmaceuticalFormsSerializer


@extend_schema_view(
    get=extend_schema(
        description='Retorna todas as formas farmacêuticas',
        responses={200: PharmaceuticalFormsSerializer}
    ),
    post=extend_schema(
        description='Criar uma forma farmacêutica',
        request=PharmaceuticalFormsSerializer,
        responses={201: PharmaceuticalFormsSerializer}
    )
)
class PharmaceuticalFormsListCreateApiView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = PharmaceuticalForms.objects.all()
    serializer_class = PharmaceuticalFormsSerializer


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de uma forma farmacêutica',
        responses={200: PharmaceuticalFormsSerializer}
    ),
    put=extend_schema(
        description='Atualiza todos os dados de uma forma farmacêutica',
        request=PharmaceuticalFormsSerializer,
        responses={200: PharmaceuticalFormsSerializer}
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de uma forma farmacêutica',
        request=PharmaceuticalFormsSerializer,
        responses={200: PharmaceuticalFormsSerializer}
    ),
    delete=extend_schema(
        description='Remove uma forma farmacêutica',
        responses={204: None}
    )
)
class PharmaceuticalFormsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = PharmaceuticalForms.objects.all()
    serializer_class = PharmaceuticalFormsSerializer
