from django.contrib import admin
from pharmaceutical_forms.models import PharmaceuticalForms


@admin.register(PharmaceuticalForms)
class PharmaceuticalFormAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'category', 'description')
    search_fields = ('id', 'name', 'category',)
