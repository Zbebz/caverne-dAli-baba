from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import ECOLES, Fichier, User
from .helper import TagField


class RegisterForm(UserCreationForm):
    ecole = forms.ChoiceField(choices=ECOLES, required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "password1", "password2", "ecole"]
        
    
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
                Row("username"),
                Row("ecole"),
                Row(Column("password1"), Column("password2")),
                StrictButton(
                    "S'inscrire",
                    type="submit",
                    css_id="submit-button",
                    css_class="btn-primary mx-auto w-auto",
                ),
                css_class="container w-50 mx-auto",
            ),
        )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = f"{user.username}@eduge.ch"
        
        if commit:
            user.save()
            
        return user
        
class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = False

        self.helper.layout = Layout(
            Field("username"),
            Field("password"),
            StrictButton(
                "Se connecter",
                type="submit",
                css_id="submit-button",
                css_class="btn btn-primary mx-auto",
            ),
        )
        
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                "Ce compte est banni.",
                code="inactive",
            )
        if not user.verified:
            raise ValidationError(
                "Ce compte n'est pas vérifié.",
                code="unverified",
            )

class FichierForm(forms.ModelForm):
    mots_cles = TagField(label="Mots clés")
    class Meta():
        model = Fichier
        exclude = ["user", "uploadDatetime", "status", "tags", "thumbnail"]
        widgets = {
            "file": forms.FileInput(
                attrs={
                    "hidden": "true",
                    "accept": ".pdf,application/pdf",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(FichierForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        
        self.helper.layout = Layout(
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
                Row(Field("mots_cles", autocomplete="off")),
                css_id="field-2",
            ),
        )
