from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.models import AbstractUser
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token

class VerificationEmail(EmailMessage):
    content_subtype = "html" # https://sendlayer.com/blog/how-to-send-email-with-django/
    def __init__(self, user: AbstractUser, *args, **kwargs):
        self.user = user
        super(VerificationEmail, self).__init__(*args, **kwargs)
        self.to = [self.user.email]
    
    def make_body(self, domain: str, is_secure=False):
        token = account_activation_token.make_token(self.user)
        self.body = render_to_string(
            "caverne/verification_email.html",
            {
                "user": self.user,
                "protocol": "https" if is_secure else "http",
                "domain": domain,
                "uid": urlsafe_base64_encode(force_bytes(self.user.pk)),
                "token": token,
            },
        )
        