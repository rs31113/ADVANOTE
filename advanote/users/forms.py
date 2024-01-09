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
                "placeholder": "Имя пользователя",
            },
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Email",
            },
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Пароль",
            },
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Повторите пароль",
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
                "placeholder": "Логин",
            },
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Пароль",
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
                attrs={"type": "date", "class": "form-control-profile"},
            ),
        }


class UserChangeForm(django.contrib.auth.forms.UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control-profile"

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
                "placeholder": "Старый пароль",
            },
        ),
        required=False,
    )
    new_password1 = django.forms.CharField(
        widget=django.forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": "Новый пароль",
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
                "placeholder": "Повторите новый пароль",
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
