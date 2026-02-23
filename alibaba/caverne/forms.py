from django import forms
from .models import Fichier

class FichierForm(forms.ModelForm):
    """Form definition for Fichier."""

    class Meta:
        """Meta definition for Fichierform."""
        model = Fichier
        # fields = ('name', 'description', 'year', 'subject', 'tags', 'file', )
        exclude = ['user', 'uploadDatetime', 'status']


