from django.db import models


TYPES = (
    ('ENT', 'Enterais'),
    ('PAR', 'Parenterais(injetáveis)'),
    ('TOP', 'Tópicos/Locais')
)


class RoutesOfAdministration(models.Model):

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=6, choices=TYPES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
