from django.contrib import admin

from .models import LegalDoc


@admin.register(LegalDoc)
class LegalDocAdmin(admin.ModelAdmin):
    """Encapsulate all admin options and functionality for LegalDoc model."""

    list_display = ("doc", "user", "up_date")
    list_filter = (
        "user",
        "up_date",
    )
