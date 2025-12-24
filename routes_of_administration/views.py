from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from app.permissions import GlobalDefaultPermissions
from routes_of_administration.models import RoutesOfAdministration
from routes_of_administration.serializers import RoutesOfAdministrationSerializer


@extend_schema_view(
    get=extend_schema(
        description='Retorna todas as vias de administração',
        responses={200: RoutesOfAdministrationSerializer},
        tags=['Vias de Administração']
    ),
    post=extend_schema(
        description='Criar uma via de administração',
        request=RoutesOfAdministrationSerializer,
        responses={201: RoutesOfAdministrationSerializer},
        tags=['Vias de Administração']
    )
)
class RoutesOfAdministrationListCreateAPIView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = RoutesOfAdministration.objects.all()
    serializer_class = RoutesOfAdministrationSerializer


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de uma via de administração',
        responses={200: RoutesOfAdministrationSerializer},
        tags=['Vias de Administração']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de uma via de administração',
        request=RoutesOfAdministrationSerializer,
        responses={200: RoutesOfAdministrationSerializer},
        tags=['Vias de Administração']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de uma via de administração',
        request=RoutesOfAdministrationSerializer,
        responses={200: RoutesOfAdministrationSerializer},
        tags=['Vias de Administração']
    ),
    delete=extend_schema(
        description='Remove uma via de administração',
        responses={204: None},
        tags=['Vias de Administração']
    )
)
class RoutesOfAdministrationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = RoutesOfAdministration.objects.all()
    serializer_class = RoutesOfAdministrationSerializer
