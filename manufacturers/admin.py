from django.contrib import admin
from manufacturers.models import Manufacturers


@admin.register(Manufacturers)
class ManufacturersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'Address', 'contact_details')
    search_fields = ('id', 'name',)
