import sys

import django.contrib.auth.models
import django.db.models

import users.manager


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    birthday = django.db.models.DateField(
        verbose_name="дата рождения",
        blank=True,
        null=True,
        db_column="birthday",
    )
    blocked_time = django.db.models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="дата заморозки",
        db_column="user_freeze",
    )
    attempts_count = django.db.models.PositiveIntegerField(
        verbose_name="попыток войти в аккаунт",
        null=False,
        blank=True,
        db_column="attempts_count",
        default=0,
    )
    email_confirm = django.db.models.BooleanField(
        verbose_name="активация почты",
        null=False,
        blank=True,
        db_column="email_confirm",
        default=False,
    )


class User(django.contrib.auth.models.User):
    objects = users.manager.UserManager()

    class Meta:
        proxy = True
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    User._meta.get_field("email")._unique = True


__all__ = ()
