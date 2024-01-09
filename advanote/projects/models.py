import django.contrib.auth.models
import django.db.models

import core.models
import notes.models
import projects.manager
import tasks.models


class Project(core.models.AbstractEntityModel):
    objects = projects.manager.ProjectManager()
    name = django.db.models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="Максимально 150 символов",
    )
    description = django.db.models.TextField(
        verbose_name="описание",
        help_text="Введите описание проекта",
        null=True,
        blank=True,
    )
    members = django.db.models.ManyToManyField(
        django.contrib.auth.models.User,
        related_name="members",
        verbose_name="участники проекта",
    )
    task = django.db.models.ManyToManyField(
        tasks.models.Task,
        related_name="tasks",
        verbose_name="задачи",
    )
    note = django.db.models.ManyToManyField(
        notes.models.Note,
        related_name="notes",
        verbose_name="заметки",
    )
    invite_link = django.db.models.CharField(
        max_length=150,
        verbose_name="пригласительная ссылка",
        help_text="Максимально 150 символов",
        null=True,
        blank=True,
    )


__all__ = ()
