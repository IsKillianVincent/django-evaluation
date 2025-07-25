from django import forms
from django.forms.widgets import ClearableFileInput
from jobs.models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "description"]

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

class CompanyImagesUploadForm(forms.Form):
    images = forms.FileField(
        required=False,
        widget=MultipleFileInput(attrs={"multiple": True}),
        label="Images de l’entreprise (max 5)"
    )
