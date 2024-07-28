import django.contrib.auth.forms


class ResetPasswordForm(django.contrib.auth.forms.PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "e-mail",
            },
        )


class SetPasswordForm(django.contrib.auth.forms.SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields["new_password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "new password",
            },
        )
        self.fields["new_password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "repeat password",
            },
        )


__all__ = ()
