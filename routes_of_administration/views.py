from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermissions
from routes_of_administration.models import RoutesOfAdministration
from routes_of_administration.serializers import RoutesOfAdministrationSerializer


class RoutesOfAdministrationListCreateAPIView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = RoutesOfAdministration.objects.all()
    serializer_class = RoutesOfAdministrationSerializer


class RoutesOfAdministrationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = RoutesOfAdministration.objects.all()
    serializer_class = RoutesOfAdministrationSerializer
