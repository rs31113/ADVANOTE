import django.contrib.auth.views
import django.urls

import authorization.views
import users.views

app_name = "authorization"
urlpatterns = [
    django.urls.path(
        "",
        authorization.views.Login.as_view(),
        name="login",
    ),
    django.urls.path(
        "signup/",
        authorization.views.Signup.as_view(),
        name="signup",
    ),
    django.urls.path(
        "emailconfirm/<uidb64>/<token>",
        authorization.views.ConfirmEmail.as_view(),
        name="email_confirm",
    ),
    django.urls.path(
        "password_reset/",
        authorization.views.ResetPassword.as_view(),
        name="password_reset",
    ),
    django.urls.path(
        "password_done/",
        authorization.views.ResetPasswordDone.as_view(),
        name="password_done",
    ),
    django.urls.path(
        "password_confirm/<uidb64>/<token>",
        authorization.views.ResetPasswordConfirm.as_view(),
        name="password_confirm",
    ),
    django.urls.path(
        "password_complete/",
        authorization.views.ResetPasswordComplete.as_view(),
        name="password_complete",
    ),
    django.urls.path(
        "profile/",
        users.views.Profile.as_view(),
        name="profile",
    ),
    django.urls.path(
        "logout/",
        django.contrib.auth.views.LogoutView.as_view(
            template_name="authorization/reset_done.html",
        ),
        name="logout",
    ),
]
