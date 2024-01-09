import django.contrib.auth.backends
import django.contrib.sites.shortcuts
import django.core.mail
import django.template.loader
import django.utils.encoding
import django.utils.http
import django.utils.timezone

import advanote.settings
import authorization.tokens
import users.models


class AuthorizationBackend(
    django.contrib.auth.backends.AllowAllUsersModelBackend,
):
    def user_can_authenticate(self, user):
        return all(
            (
                user.is_active,
                user.profile.email_confirm,
            ),
        )

    @staticmethod
    def user_login(user, request):
        subject_mail = "Кто - то вошёл в ваш аккаунт!"
        message = django.template.loader.render_to_string(
            "authorization/account_login.html",
            {
                "name": user.username,
                "domain": django.contrib.sites.shortcuts.get_current_site(
                    request,
                ).domain,
                "uid": django.utils.http.urlsafe_base64_encode(
                    django.utils.encoding.force_bytes(user.pk),
                ),
                "token": (
                    authorization.tokens.account_activation_token.make_token
                )(
                    user,
                ),
                "protocol": "https" if request.is_secure() else "http",
            },
        )
        django.core.mail.send_mail(
            subject_mail,
            message,
            advanote.settings.DJANGO_MAIL,
            [user.email],
            fail_silently=False,
        )

    @staticmethod
    def get_user_by_email(username):
        try:
            mail = users.models.User.objects.normalize_email(username)
            get_user = users.models.User.objects.get(email=mail)
            return get_user
        except users.models.User.DoesNotExist:
            return False

    @staticmethod
    def get_user_by_username(username):
        try:
            get_user = users.models.User.objects.get(username=username)
            return get_user
        except users.models.User.DoesNotExist:
            return False

    def get_user_object(self, username):
        for user in (
            self.get_user_by_username,
            self.get_user_by_email,
        ):
            user = user(username)
            if user:
                return user
        raise users.models.User.DoesNotExist

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            get_user = self.get_user_object(username)
        except users.models.User.DoesNotExist:
            return None
        else:
            if not self.user_can_authenticate(get_user):
                return None

            if get_user.check_password(password):
                if not (
                    users.models.Profile.objects.filter(user=get_user).exists()
                ):
                    users.models.Profile.objects.create(
                        user=get_user,
                    )
                    get_user = users.models.User.objects.get(pk=get_user.id)
                self.user_login(get_user, request)
                return get_user

        return None


__all__ = ()
