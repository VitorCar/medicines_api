import os
import datetime
from django.core.management.base import BaseCommand, CommandError
from drug_identification.models import DrugIdentification
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from app.settings import BASE_DIR


class Command(BaseCommand):
   

    def add_arguments(self, parser):
      parser.add_argument(
        'id_drug',
        type=int,
        help='ID do remédio a ser gerado uma bula.pdf, caso não saiba o iD expecifico utilize o comando python manage.py get_id'
      )

    def handle(self, *args, **options):
      id_drug = options['id_drug']

      try: 
         
        obj = DrugIdentification.objects.get(pk=id_drug)
        current_time = datetime.datetime.now()
        self.stdout.write(self.style.SUCCESS(f'Sucesso: objeto {obj.trade_name} encontrado (ID: {obj.id})'))

        file_name = os.path.join(BASE_DIR, f'Bula_{obj.trade_name}.pdf')
        doc = SimpleDocTemplate(file_name, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(f"<b>{obj.trade_name}</b>", styles['Title']))
        story.append(Spacer(1, 12))

        story.append(Paragraph(f"<b>Nome Genérico:</b> {obj.generic_name}", styles['Normal']))
        story.append(Spacer(1, 6))

        type_display = obj.get_type_of_medicine_display()
        story.append(Paragraph(f"<b>Tipo de Medicamento:</b> {type_display}", styles['Normal']))
        story.append(Spacer(1, 6))

        if obj.indications:
            story.append(Paragraph(f"<b>Indicações:</b> {obj.indications}", styles['Normal']))
            story.append(Spacer(1, 6))

        forms = ', '.join([form.name for form in obj.pharmaceutical_form.all()])
        story.append(Paragraph(f"<b>Forma Farmacêutica:</b> {forms}", styles['Normal']))
        story.append(Spacer(1, 6))

        story.append(Paragraph(f"<b>Apresentação:</b> {obj.presentation}", styles['Normal']))
        story.append(Spacer(1, 6))

        routes = ', '.join([route.name for route in obj.routes_of_administration.all()])
        story.append(Paragraph(f"<b>Via de Administração:</b> {routes}", styles['Normal']))
        story.append(Spacer(1, 6))

        story.append(Paragraph(f"<b>Princípio Ativo:</b> {obj.active_ingredient}", styles['Normal']))
        story.append(Spacer(1, 6))

        if obj.concentration:
            story.append(Paragraph(f"<b>Concentração:</b> {obj.concentration}", styles['Normal']))
            story.append(Spacer(1, 6))

        story.append(Paragraph(f"<b>Cuidados de Armazenamento:</b> {obj.storage_care}", styles['Normal']))
        story.append(Spacer(1, 6))

        prescription_display = obj.get_medical_prescription_display()
        observation_prescription = 'VENDA SOB PRESCRIÇÃO MÉDICA' if obj.medical_prescription == 'SIM' else ''
        story.append(Paragraph(f"<b>Prescrição Médica:</b> {prescription_display}", styles['Normal']))
        if observation_prescription:
            story.append(Paragraph(f"<i>{observation_prescription}</i>", styles['Normal']))
        story.append(Spacer(1, 6))

        doping_display = obj.get_doping_alert_display()
        observation_doping = 'ESTE PRODUTO CONTÉM SUBSTÂNCIAS QUE PODEM CAUSAR DOPING' if obj.doping_alert == 'SIM' else ''
        story.append(Paragraph(f"<b>Alerta de Doping:</b> {doping_display}", styles['Normal']))
        if observation_doping:
            story.append(Paragraph(f"<i>{observation_doping}</i>", styles['Normal']))
        story.append(Spacer(1, 6))

        if obj.contraindications:
            story.append(Paragraph(f"<b>Contraindicações:</b> {obj.contraindications}", styles['Normal']))
            story.append(Spacer(1, 6))

        if obj.precautions_and_warnings:
            story.append(Paragraph(f"<b>Precauções e Advertências:</b> {obj.precautions_and_warnings}", styles['Normal']))
            story.append(Spacer(1, 6))

        if obj.adverse_reactions:
            story.append(Paragraph(f"<b>Reações Adversas:</b> {obj.adverse_reactions}", styles['Normal']))
            story.append(Spacer(1, 6))

        story.append(Paragraph(f"<b>Valor Estimado:</b> {obj.estimated_value}", styles['Normal']))
        story.append(Spacer(1, 6))

        manufacturers = ', '.join([man.name for man in obj.manufacturers.all()])
        story.append(Paragraph(f"<b>Fabricantes:</b> {manufacturers}", styles['Normal']))
        story.append(Spacer(1, 6))

        if obj.batch_number:
            story.append(Paragraph(f"<b>Lote:</b> {obj.batch_number}", styles['Normal']))
            story.append(Spacer(1, 6))

        if obj.manufacturing_date:
            story.append(Paragraph(f"<b>Data de Fabricação:</b> {obj.manufacturing_date.strftime('%d/%m/%Y')}", styles['Normal']))
            story.append(Spacer(1, 6))

        if obj.validity:
            story.append(Paragraph(f"<b>Validade:</b> {obj.validity.strftime('%d/%m/%Y')}", styles['Normal']))
            story.append(Spacer(1, 6))

        story.append(Paragraph(f"<b>Criado em:</b> {obj.created_at.strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 6))

        story.append(Paragraph(f"<b>Atualizado em:</b> {obj.updated_at.strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 6))

        story.append(Paragraph(f"<b> Bula emitida em:</b> {current_time.strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 6))

        doc.build(story)
        os.startfile(file_name)

      except DrugIdentification.DoesNotExist:
        raise CommandError (f"Objeto com ID {id_drug} não existe.")
