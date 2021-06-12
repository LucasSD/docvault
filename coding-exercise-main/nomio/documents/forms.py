from django import forms
from .models import LegalDoc


class UserUploadForm(forms.ModelForm):
    class Meta:
        model = LegalDoc
        fields = [
            "doc",
        ]
