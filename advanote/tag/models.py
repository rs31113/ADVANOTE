import posixpath

import django.db.models
import sorl.thumbnail


def tag_image_path(instance, filename):
    return posixpath.join(
        "tag",
        "main_image",
        instance.item.name,
        filename,
    )


class Tag(django.db.models.Model):
    name = django.db.models.TextField(
        max_length=150,
        verbose_name="название",
        help_text="Максимально 150 символов",
        unique=True,
    )
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="опубликовано",
    )


class MainImage(django.db.models.Model):
    image = django.db.models.ImageField(upload_to=tag_image_path)
    tag = django.db.models.OneToOneField(
        Tag,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
        related_query_name="main_image",
    )

    def get_image_(self, x, y):
        return sorl.thumbnail.get_thumbnail(self.image, f"{x}x{y}", quality=51)

    class Meta:
        verbose_name = "главное фото тега"
        verbose_name_plural = "главные фотографии тегов"


__all__ = ()
