from django import forms

from .models import LegalDoc


class UserUploadForm(forms.ModelForm):
    """Model form to instantiate a LegalDoc model object."""

    class Meta:
        model = LegalDoc
        fields = [
            "doc",
        ]

        widgets = {"doc": forms.ClearableFileInput(attrs={"multiple": True})}
