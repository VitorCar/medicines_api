from django.core.management.base import BaseCommand
from drug_identification.models import DrugIdentification


class Command(BaseCommand):

    def handle(self, *args, **options):
        objects = DrugIdentification.objects.all()

        for obj in objects:
            self.stdout.write(self.style.SUCCESS(f"Sucesso: Objeto {obj.trade_name} encontrado (ID: {obj.id})"))
