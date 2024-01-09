import django.contrib.auth.models
import django.db.models


class AbstractEntityModel(django.db.models.Model):
    owner = django.db.models.ForeignKey(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
        verbose_name="создатель",
        null=False,
        blank=False,
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания",
        null=True,
    )
    updated_at = django.db.models.DateTimeField(
        auto_now=True,
        verbose_name="дата изменения",
        null=True,
    )

    class Meta:
        abstract = True


__all__ = ()
