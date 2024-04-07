# Generated by Django 4.2 on 2024-04-07 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tasks", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        null=True,
                        verbose_name="дата создания",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="дата изменения"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Максимально 150 символов",
                        max_length=150,
                        verbose_name="название",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Введите описание проекта",
                        null=True,
                        verbose_name="описание",
                    ),
                ),
                (
                    "invite_link",
                    models.CharField(
                        blank=True,
                        help_text="Максимально 150 символов",
                        max_length=150,
                        null=True,
                        verbose_name="пригласительная ссылка",
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        related_name="members",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="участники проекта",
                    ),
                ),
                (
                    "note",
                    models.ManyToManyField(
                        related_name="notes",
                        to="notes.note",
                        verbose_name="заметки",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="создатель",
                    ),
                ),
                (
                    "task",
                    models.ManyToManyField(
                        related_name="tasks",
                        to="tasks.task",
                        verbose_name="задачи",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
