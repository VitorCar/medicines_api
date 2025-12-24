from django.db import models


CATEGORY = (
    ('SOL', 'Sólidos'),
    ('LIQ', 'Líquidos'),
    ('SEM', 'Semissólidos'),
    ('GAS', 'Gasosos')
)


class PharmaceuticalForms(models.Model):

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=6, choices=CATEGORY)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
