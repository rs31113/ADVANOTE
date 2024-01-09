# Generated by Django 4.2 on 2023-12-21 16:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0004_project_description_alter_project_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="invite_link",
            field=models.CharField(
                blank=True,
                help_text="Максимально 150 символов",
                max_length=150,
                null=True,
                verbose_name="ссылка прилашения",
            ),
        ),
    ]


__all__ = ()