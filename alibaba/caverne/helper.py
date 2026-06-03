from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.db.models import Func, TextField
from django.template.loader import render_to_string
from django.utils.crypto import constant_time_compare
from django.utils.encoding import force_bytes
from django.utils.http import base36_to_int, urlsafe_base64_encode

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.verified}"

    def check_token(self, user, token):
        # Même fonction que celle de base
        # Seule modif.: retourne 1 si le token est valide mais expiré et 0 sinon
        # Et -1 si tout va bien
        if not (user and token):
            return False, 0

        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False, 0

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False, 0

        for secret in [self.secret, *self.secret_fallbacks]:
            if constant_time_compare(
                self._make_token_with_timestamp(user, ts, secret),
                token,
            ):
                break
        else:
            return False, 0

        # Check the timestamp is within limit.
        if (self._num_seconds(self._now()) - ts) > settings.PASSWORD_RESET_TIMEOUT:
            return False, 1

        return True, -1

account_activation_token = AccountActivationTokenGenerator()


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

class ArrayToString(Func):
    """Convert tags to a string"""
    function="array_to_string"
    output_field=TextField()
