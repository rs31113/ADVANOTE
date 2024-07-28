import django.contrib
from django.contrib.auth import login as auth_login
import django.contrib.auth.models
import django.contrib.auth.views
import django.contrib.messages
import django.contrib.sites.shortcuts
import django.core.mail
import django.http
import django.shortcuts
import django.template.loader
import django.urls
import django.utils.encoding
import django.utils.http
import django.views

import advanote.settings
import authorization.forms
import authorization.tokens
import users.forms
import users.models


class Signup(django.views.generic.FormView):
    template_name = "authorization/signup.html"
    form_class = users.forms.SingUpForm
    success_url = django.urls.reverse_lazy("authorization:login")

    def activate_email(self, user, email):
        subject_mail = "Подтверждение почты."
        message = django.template.loader.render_to_string(
            "authorization/activate_email.html",
            {
                "name": user.username,
                "domain": django.contrib.sites.shortcuts.get_current_site(
                    self.request,
                ).domain,
                "uid": django.utils.http.urlsafe_base64_encode(
                    django.utils.encoding.force_bytes(user.pk),
                ),
                "token": (
                    authorization.tokens.account_activation_token.make_token
                )(
                    user,
                ),
                "protocol": "https" if self.request.is_secure() else "http",
            },
        )
        django.core.mail.send_mail(
            subject_mail,
            message,
            advanote.settings.DJANGO_MAIL,
            [email],
            fail_silently=False,
        )

    def form_valid(self, form):
        user = django.contrib.auth.models.User.objects.create_user(
            password=form.cleaned_data.get("password1"),
            email=form.cleaned_data.get("email"),
            username=form.cleaned_data.get("username"),
            is_active=True,
        )
        user.save()
        profile = users.models.Profile.objects.create(user=user)
        profile.save()
        self.activate_email(user, form.cleaned_data.get("email"))
        django.contrib.messages.success(
            self.request,
            "Thank you for signing up, please check your email!",
        )
        return super().form_valid(form)


class Login(django.views.generic.FormView):
    template_name = "authorization/login.html"
    form_class = users.forms.LogInForm
    success_url = django.urls.reverse_lazy("today:today")

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return super().form_valid(form)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())


class ConfirmEmail(django.views.generic.View):
    def get(self, request, *args, **kwargs):
        user, valid = authorization.tokens.account_activation_token.get_user(
            kwargs["uidb64"],
            kwargs["token"],
        )

        if valid and user.profile.email_confirm:
            return django.shortcuts.redirect("today:today")

        if valid:
            user.profile.email_confirm = True
            user.profile.save()
            django.contrib.messages.success(
                request,
                "Thank you for confirming your email!"
                "Now you can log in to your account!",
            )
            return django.shortcuts.redirect("authorization:login")

        django.contrib.messages.error(
            request,
            "The activation link is no longer valid!",
        )
        return django.shortcuts.redirect("authorization:login")


class ResetPassword(django.contrib.auth.views.PasswordResetView):
    template_name = "authorization/reset_password.html"
    email_template_name = "authorization/password_reset_email.html"
    subject_template_name = "authorization/password_reset_email_subject.txt"
    success_url = django.urls.reverse_lazy("authorization:password_done")
    token_generator = authorization.tokens.account_activation_token
    form_class = authorization.forms.ResetPasswordForm


class ResetPasswordDone(django.contrib.auth.views.PasswordResetDoneView):
    template_name = "authorization/reset_done.html"


class ResetPasswordConfirm(django.contrib.auth.views.PasswordResetConfirmView):
    success_url = django.urls.reverse_lazy("authorization:password_complete")
    token_generator = authorization.tokens.account_activation_token
    template_name = "authorization/reset_confirm.html"
    form_class = authorization.forms.SetPasswordForm


class ResetPasswordComplete(
    django.contrib.auth.views.PasswordResetCompleteView,
):
    template_name = "authorization/reset_done.html"


__all__ = ()
