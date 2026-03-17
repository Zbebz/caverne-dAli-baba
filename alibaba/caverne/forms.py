from django import forms

from .models import Fichier


class FichierForm(forms.ModelForm):

    class Meta:
        model = Fichier
        exclude = ["user", "uploadDatetime", "status"]
        widgets = {
            "file": forms.FileInput(attrs={"hidden": "true"}),
            "annotated": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super(FichierForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            if hasattr(field, "choices"):
                attributes = {"class": "form-select"}
                field.widget.attrs.update(attributes)
                choices = list(field.choices)[1:]
                field.choices = [
                    ("", f"Choisissez un.e {field.label.lower()}")
                ] + choices
                
            attributes = {"class": "form-control"}
            for attr in attributes:
                attributes[attr] = field.widget.attrs.get(
                    attr, attributes[attr]
                )
                field.widget.attrs.update(attributes)
                attributes = {"class": "form-control"}
