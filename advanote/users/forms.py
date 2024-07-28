import django.contrib.auth.forms
import django.contrib.auth.models
from django.contrib.auth.password_validation import (
    password_validators_help_text_html,
)
import django.forms

import users.models


class SingUpForm(django.contrib.auth.forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "username",
            },
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "e-mail",
            },
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "password",
            },
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "repeat password",
            },
        )

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = django.contrib.auth.models.User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class LogInForm(django.contrib.auth.forms.AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "username",
            },
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "password",
            },
        )


class ProfileChangeForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            users.models.Profile.birthday.field.name
        ].initial = self.instance.birthday

    class Meta:
        model = users.models.Profile
        fields = (users.models.Profile.birthday.field.name,)
        widgets = {
            users.models.Profile.birthday.field.name: django.forms.DateInput(
                attrs={"type": "date", "class": "form-control"},
            ),
        }


class UserChangeForm(django.contrib.auth.forms.UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "username",
            },
        )
        self.fields["first_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "name",
            },
        )
        self.fields["last_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "surname",
            },
        )

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = django.contrib.auth.models.User
        fields = (
            django.contrib.auth.models.User.username.field.name,
            django.contrib.auth.models.User.first_name.field.name,
            django.contrib.auth.models.User.last_name.field.name,
        )


class PasswordChangeForm(django.contrib.auth.forms.PasswordChangeForm):
    old_password = django.forms.CharField(
        strip=False,
        widget=django.forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-control",
                "placeholder": "old password",
            },
        ),
        required=False,
    )
    new_password1 = django.forms.CharField(
        widget=django.forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "new password",
            },
        ),
        strip=False,
        required=False,
        help_text=password_validators_help_text_html(),
    )
    new_password2 = django.forms.CharField(
        strip=False,
        widget=django.forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "repeat new password",
            },
        ),
        required=False,
    )

    def is_valid(self):
        if not self.changed_data:
            return True
        return super().is_valid()

    def save(self, commit=True):
        if self.changed_data:
            super().save(commit)


__all__ = ()
