from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        # Campos reales de tu modelo (owner se asigna en la vista)
        fields = ['name', 'category', 'criticality', 'status']