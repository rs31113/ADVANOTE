import django.db.models

import core.models
import notes.manager
import tag.models


class Note(core.models.AbstractEntityModel):
    objects = notes.manager.NoteManager()

    title = django.db.models.TextField(
        max_length=150,
        verbose_name="название",
        help_text="Максимально 150 символов",
        null=False,
        blank=False,
    )
    text = django.db.models.TextField(
        verbose_name="текст заметки",
        help_text="Запишите сюда текст заметки",
        null=True,
        blank=True,
    )
    tags = django.db.models.ManyToManyField(
        tag.models.Tag,
        verbose_name="теги",
        related_name="note_tags",
        blank=True,
    )

    def __str__(self):
        return self.title


__all__ = ()
