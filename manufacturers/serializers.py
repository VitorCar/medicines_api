from rest_framework import serializers
from manufacturers.models import Manufacturers


class ManufacturersSerializer(serializers.ModelSerializer):

    class Meta:

        model = Manufacturers
        fields = '__all__'
