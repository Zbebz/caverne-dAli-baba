from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Field, Layout, Row
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse

from .models import Fichier, User


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        # https://stackoverflow.com/questions/34144277/avoid-display-of-help-text-in-django-crispy-forms
        for field_name, _ in self.fields.items():
            self.fields[field_name].help_text = None
        
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_action = reverse("register")
        
        self.helper.layout = Layout(
            Div(
                Field("username", wrapper_class="mx-auto w-auto"),
                Field("password1", wrapper_class="mx-auto w-auto"),
                Field("password2", wrapper_class="mx-auto w-auto"),
                StrictButton(
                    "S'inscrire",
                    type="submit",
                    css_id="submit-button",
                    css_class="btn-primary mx-auto w-auto",
                ),
                css_class="d-flex flex-column justify-content-center",
            ),
        )
    
        
class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        
        self.helper.layout = Layout(
            Div(
                Field("username", wrapper_class="mx-auto w-auto"),
                Field("password", wrapper_class="mx-auto w-auto"),
                StrictButton(
                    "Se connecter",
                    type="submit",
                    css_id="submit-button",
                    css_class="btn-primary mx-auto w-auto",
                ),
                css_class="d-flex flex-column justify-content-center",
            ),
        )

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
                    Row(Field("name", autocomplete="off")),
                    Row(Column("year"), Column("subject")),
                    Row("type"),
                    Row(Column("ecole"), Column(Field("enseignant", autocomplete="off"))),
                    Row("annotated"),
                    css_id="field-1",
                ),
                Div(
                    Row(Field("description", autocomplete="off")),
                    Row(Field("tags", autocomplete="off")),
                    css_id="field-2",
                ),
                StrictButton(
                    "Continuer",
                    css_id="submit-button",
                    css_class="btn-primary",
                ),
                css_class="container w-50 mt-5 ms-5",
            ),
        )
