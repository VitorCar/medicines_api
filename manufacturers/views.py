from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermissions
from manufacturers.models import Manufacturers
from manufacturers.serializers import ManufacturersSerializer


class ManufacturersListCreateAPIView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = Manufacturers.objects.all()
    serializer_class = ManufacturersSerializer


class ManufacturersRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, GlobalDefaultPermissions,)
    queryset = Manufacturers
    serializer_class = ManufacturersSerializer
