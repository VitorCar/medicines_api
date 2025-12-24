from rest_framework import serializers
from drug_identification.models import DrugIdentification
from pharmaceutical_forms.serializers import PharmaceuticalFormsSerializer
from routes_of_administration.serializers import RoutesOfAdministrationSerializer
from manufacturers.serializers import ManufacturersSerializer


class DrugIdentificationSerializer(serializers.ModelSerializer):


    class Meta:

        model = DrugIdentification
        fields = '__all__'


class DrugIdentificationListSerializer(serializers.ModelSerializer):
    pharmaceutical_form = PharmaceuticalFormsSerializer(many=True)
    routes_of_administration = RoutesOfAdministrationSerializer(many=True)
    manufacturers = ManufacturersSerializer(many=True)
    observation_doping = serializers.SerializerMethodField(read_only=True)
    observation_prescription = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model= DrugIdentification
        fields = [
            'id',
            'trade_name',
            'generic_name',
            'type_of_medicine',
            'indications',
            'pharmaceutical_form',
            'presentation',
            'routes_of_administration',
            'active_ingredient',
            'concentration',
            'storage_care',
            'medical_prescription',
            'observation_prescription',
            'doping_alert',
            'observation_doping',
            'contraindications',
            'precautions_and_warnings',
            'adverse_reactions',
            'estimated_value',
            'manufacturers',
            'batch_number',
            'manufacturing_date',
            'validity',
            'created_at',
            'updated_at',
        ]

    def get_observation_doping(self, obj):
        if obj.doping_alert == 'SIM':
           return 'ESTE PRODUTO CONTÉM SUBSTÂNCIAS QUE PODEM CAUSAR DOPING'
        return None

    def get_observation_prescription(self, obj):
        if obj.medical_prescription == 'SIM':
            return 'VENDA SOB PRESCRIÇÃO MÉDICA'
        return None
