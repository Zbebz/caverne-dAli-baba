from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int


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