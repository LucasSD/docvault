from django.contrib import admin
from .models import LegalDoc


@admin.register(LegalDoc)
class LegalDocAdmin(admin.ModelAdmin):
    pass
