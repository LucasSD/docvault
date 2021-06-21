from django.contrib import admin

from .models import LegalDoc, Tag


@admin.register(LegalDoc)
class LegalDocAdmin(admin.ModelAdmin):
    """Encapsulate all admin options and functionality for LegalDoc model."""

    list_display = (
        "doc",
        "user",
        "up_date",
        "display_tag"
    )
    list_filter = ("user", "up_date", "tag")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Encapsulate all admin options and functionality for Tag model."""
