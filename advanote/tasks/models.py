import django.db.models

import core.models
import tag.models
import tasks.manager


class Task(core.models.AbstractEntityModel):
    objects = tasks.manager.TasksManager()
    POINT_CHOICES = [
        (1, "Главный"),
        (2, "Средний"),
        (3, "Неважный"),
    ]
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
        related_name="task_tags",
        blank=True,
    )
    priority = django.db.models.IntegerField(
        choices=POINT_CHOICES,
        db_column="priority",
        verbose_name="приоритет",
        blank=False,
        null=False,
        default=3,
    )
    is_done = django.db.models.BooleanField(default=False)

    def __str__(self):
        return self.title


__all__ = ()
