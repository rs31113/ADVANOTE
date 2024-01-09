import django.contrib.auth.tokens
import django.utils.encoding
import django.utils.http
import six

import users.models


class TokenGenerator(
    django.contrib.auth.tokens.PasswordResetTokenGenerator,
):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active),
        )

    def get_user(self, uidb64, token):
        try:
            uid = django.utils.encoding.force_str(
                django.utils.http.urlsafe_base64_decode(uidb64),
            )
            user = users.models.User.objects.get(pk=uid)
            valid = self.check_token(user, token)
        except (
            TypeError,
            ValueError,
            OverflowError,
            users.models.User.DoesNotExist,
        ):
            user = None
            valid = False
        return user, valid


account_activation_token = TokenGenerator()

__all__ = ()
