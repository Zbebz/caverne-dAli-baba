from django import forms

from .models import Fichier


class FichierForm(forms.ModelForm):

    class Meta:
        model = Fichier
        exclude = ['user', 'uploadDatetime', 'status']
        
        widgets = {
            'file': forms.FileInput(attrs={'hidden': 'true'})
        }


