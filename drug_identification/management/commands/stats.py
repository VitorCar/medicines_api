from django.core.management.base import BaseCommand
from django.conf import settings
from drug_identification.views import DrugIdentificationStatsView
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
import datetime

class Command(BaseCommand):
    help = 'Gera um PDF com as estatísticas de identificação de medicamentos'

    def add_arguments(self, parser):
        parser.add_argument('--output', '-o', type=str, help='Caminho do arquivo PDF de saída')

    def handle(self, *args, **options):
        output = options.get('output')
        
        if not output:
            base = getattr(settings, 'BASE_DIR', os.getcwd())
            output = os.path.join(base, 'drug_identification_stats.pdf')

        nome_base, extensao = os.path.splitext(output)
        
        carimbo_tempo = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        output = f"{nome_base}_{carimbo_tempo}{extensao}"

        view = DrugIdentificationStatsView()
        
        resp = view.get(None)
        data = getattr(resp, 'data', resp)

        c = canvas.Canvas(output, pagesize=A4)
        width, height = A4
        y = height - 50
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Drug Identification Stats")
        c.setFont("Helvetica", 10)
        y -= 30
        
        c.drawString(50, y, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 20

        for key, value in (data.items() if isinstance(data, dict) else []):
            if y < 100:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, f"{key}:")
            y -= 15
            c.setFont("Helvetica", 10)

            if hasattr(value, '__iter__') and not isinstance(value, (str, bytes, dict)):
                for item in value:
                    text = str(item)
                    if y < 80:
                        c.showPage()
                        y = height - 50
                        c.setFont("Helvetica", 10)
                    c.drawString(70, y, text)
                    y -= 12
                y -= 8
            else:
                if y < 80:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 10)
                c.drawString(70, y, str(value))
                y -= 20

        c.save()
        self.stdout.write(self.style.SUCCESS(f"PDF gerado: {output}"))