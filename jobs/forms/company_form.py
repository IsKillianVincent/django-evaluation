from django import forms
from jobs.models import Company, CompanyImage

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "description"]

class CompanyImageForm(forms.ModelForm):
    class Meta:
        model = CompanyImage
        fields = ["image", "caption"]