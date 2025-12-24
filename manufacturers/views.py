from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from app.permissions import GlobalDefaultPermissions
from manufacturers.models import Manufacturers
from manufacturers.serializers import ManufacturersSerializer


@extend_schema_view(
    get=extend_schema(
        description='Retorna todos os fabricantes e seus dados',
        responses={200: ManufacturersSerializer}
    ),
    post=extend_schema(
        description='Criar um fabricante',
        request=ManufacturersSerializer,
        responses={200: ManufacturersSerializer}
    )
)
class ManufacturersListCreateAPIView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = Manufacturers.objects.all()
    serializer_class = ManufacturersSerializer

@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de um fabricante específico',
        responses={200: ManufacturersSerializer}
    ),
    put=extend_schema(
        description='Atualiza todos os dados de um fabricante',
        request=ManufacturersSerializer,
        responses={200: ManufacturersSerializer}
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de um fabricante',
        request=ManufacturersSerializer,
        responses={200, ManufacturersSerializer}
    ),
    delete=extend_schema(
        description='Remove um fabricante do sistema',
        responses={204: None}
    )
)
class ManufacturersRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = Manufacturers
    serializer_class = ManufacturersSerializer
