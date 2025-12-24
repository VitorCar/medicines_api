from django.contrib import admin
from routes_of_administration.models import RoutesOfAdministration


@admin.register(RoutesOfAdministration)
class RoutesOfAdministrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'description')
    search_fields = ('name', 'type', 'id',)
