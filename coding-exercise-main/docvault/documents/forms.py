from django import forms

from .models import LegalDoc, Tag


class UserUploadForm(forms.ModelForm):
    """Model form to instantiate a LegalDoc model object."""

    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = LegalDoc

        fields = ["doc", "tag"]

        widgets = {"doc": forms.ClearableFileInput(attrs={"multiple": True})}
