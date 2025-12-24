from rest_framework import serializers
from pharmaceutical_forms.models import PharmaceuticalForms


class PharmaceuticalFormsSerializer(serializers.ModelSerializer):

    class Meta:

        model = PharmaceuticalForms
        fields = '__all__'
