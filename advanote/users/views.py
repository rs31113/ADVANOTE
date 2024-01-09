import django.contrib.auth.forms
import django.contrib.auth.mixins
import django.contrib.messages
import django.shortcuts
import django.urls
import django.views.generic

import users.forms
import users.models


class Profile(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.FormView,
):
    template_name = "users/profile.html"
    user_form_class = users.forms.UserChangeForm
    profile_form_class = users.forms.ProfileChangeForm
    password_change_form_class = users.forms.PasswordChangeForm
    success_url = django.urls.reverse_lazy("authorization:profile")

    def get_context_data(self, **kwargs):
        if "user_form_class" not in kwargs:
            kwargs["user_form"] = self.user_form_class(
                **self.get_form_kwargs(),
            )
        if "profile_form_class" not in kwargs:
            kwargs["profile_form"] = self.profile_form_class(
                **self.get_form_kwargs(),
            )
        if "password_change_form_class" not in kwargs:
            kwargs["password_change_form"] = self.password_change_form_class(
                **self.get_form_kwargs(),
            )

        kwargs.setdefault("view", self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)

        return kwargs

    def get(self, request, *args, **kwargs):
        user = users.models.User.objects.get_user(request.user.id)
        user = django.shortcuts.get_object_or_404(user)
        user_form = self.user_form_class(
            instance=user,
        )
        profile_form = self.profile_form_class(
            instance=user.profile,
        )
        change_password_form = self.password_change_form_class(
            user=user,
        )
        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "change_password_form": change_password_form,
        }
        return django.shortcuts.render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = users.models.User.objects.get_user(request.user.id)
        user = django.shortcuts.get_object_or_404(user)
        user_form = self.user_form_class(
            **self.get_form_kwargs(),
            instance=user,
        )
        profile_form = self.profile_form_class(
            **self.get_form_kwargs(),
            instance=user.profile,
        )
        change_password_form = self.password_change_form_class(
            **self.get_form_kwargs(),
            user=user,
        )

        if all(
            (
                user_form.is_valid(),
                profile_form.is_valid(),
                change_password_form.is_valid(),
            ),
        ):
            return self.form_valid(
                [
                    user_form,
                    profile_form,
                    change_password_form,
                ],
            )

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "change_password_form": change_password_form,
        }
        return django.shortcuts.render(request, self.template_name, context)

    def form_valid(self, forms):
        user_form = forms[0]
        profile_form = forms[1]
        change_password_form = forms[2]
        user_form.username = user_form.cleaned_data.get("username")
        user_form.email = user_form.cleaned_data.get("email")
        user_form.first_name = user_form.cleaned_data.get("first_name")
        user_form.last_name = user_form.cleaned_data.get("last_name")
        user_form.save()
        profile_form.save()
        change_password_form.save()
        django.contrib.messages.success(self.request, "Профиль обновлён!")
        return super().form_valid(forms)


__all__ = ()
