from django.db import models
from pharmaceutical_forms.models import PharmaceuticalForms
from routes_of_administration.models import RoutesOfAdministration
from manufacturers.models import Manufacturers


TYPES = (
    ('REF', 'Medicamento de Referência'),
    ('GEN', 'Medicamento Genérico'),
    ('SIM', 'Medicamento Similar')
)

OPTION = (
    ('SIM', 'Sim'),
    ('NAO', 'Não')
)


class DrugIdentification(models.Model):

    trade_name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255)
    type_of_medicine = models.CharField(max_length=50, choices=TYPES)
    pharmaceutical_form = models.ManyToManyField(PharmaceuticalForms, related_name='identification')
    indications = models.TextField(blank=True, null=True)
    routes_of_administration = models.ManyToManyField(RoutesOfAdministration, related_name='identification')
    presentation = models.CharField(max_length=500)
    active_ingredient = models.CharField(max_length=500)
    concentration = models.CharField(max_length=200, blank=True, null=True)
    storage_care = models.TextField()
    medical_prescription = models.CharField(max_length=3, choices=OPTION)
    doping_alert = models.CharField(max_length=3, choices=OPTION)
    contraindications = models.TextField(null=True, blank=True)
    precautions_and_warnings = models.TextField(null=True, blank=True)
    adverse_reactions = models.TextField(null=True, blank=True)
    manufacturers = models.ManyToManyField(Manufacturers, related_name='identification')
    estimated_value = models.CharField(max_length=100)
    batch_number = models.CharField(null=True, blank=True)
    manufacturing_date = models.DateField(null=True, blank=True)
    validity = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trade_name} ({self.generic_name})"
