from django import forms

from .models import Fichier


class FichierForm(forms.ModelForm):

    class Meta:
        model = Fichier
        exclude = ['user', 'uploadDatetime', 'status']
        widgets = {
            'file': forms.FileInput(attrs={'hidden': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        super(FichierForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if hasattr(self.fields[field_name], "choices"):
                l = list(self.fields[field_name].choices)[1:]
                print(l, flush=True)
                self.fields[field_name].choices = [
                    ("", f"Choisissez un.e {field.label.lower()}")
                ] + l
