from django.db import models


class Manufacturers(models.Model):

    name = models.CharField(max_length=100)
    Address = models.CharField(max_length=200, blank=True, null=True)
    contact_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
