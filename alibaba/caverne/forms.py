from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Layout, Row
from django import forms
from django.urls import reverse

from .models import Fichier


class FichierForm(forms.ModelForm):

    class Meta():
        model = Fichier
        exclude = ["user", "uploadDatetime", "status"]
        widgets = {
            "file": forms.FileInput(
                attrs={
                    "hidden": "true",
                    "accept": ".pdf,application/pdf,.doc,.docx,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,.odt,application/vnd.oasis.opendocument.text",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(FichierForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_action = reverse("upload")
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            HTML(
                """
<div id="file-field">
    <div id="drop-area">
        <label for="{{ form.file.id_for_label }}">
            Choisissez votre fichier
        </label>
        <span class="small-text">ou glissez-le</span>
        <span class="files-accepted"
        {% if form.file.errors %}
            style="color: red;"
        {% endif %}
            >Seulement les fichiers pdf, docx, doc, odt sont autorisés</span>
        {{ form.file }}
    </div>
</div>
"""
            ),
            Div(
                Div(
                    Row("name"),
                    Row(Column("year"), Column("subject")),
                    Row("type"),
                    Row(Column("ecole"), Column("enseignant")),
                    Row("annotated"),
                    css_id="field-1",
                ),
                Div(
                    Row("description"),
                    Row("tags"),
                    css_id="field-2",
                ),
                css_class="container w-50 mt-5 ms-5",
            ),
            StrictButton("Continuer",
                css_id="submit-button",
                css_class="btn-primary ms-5",
            ),
        )
