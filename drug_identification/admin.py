from django.contrib import admin
from drug_identification.models import DrugIdentification


@admin.register(DrugIdentification)
class DrugIdentificationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'trade_name',
        'generic_name',
        'type_of_medicine',
        'indications',
        'presentation',
        'active_ingredient',
        'concentration',
        'storage_care',
        'medical_prescription',
        'doping_alert',
        'contraindications',
        'precautions_and_warnings',
        'adverse_reactions',
        'estimated_value',
        'batch_number',
        'manufacturing_date',
        'validity',
        'created_at',
        'updated_at',
    )
