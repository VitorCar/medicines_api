from rest_framework import serializers
from routes_of_administration.models import RoutesOfAdministration


class RoutesOfAdministrationSerializer(serializers.ModelSerializer):

    class Meta:

        model = RoutesOfAdministration
        fields = '__all__'
