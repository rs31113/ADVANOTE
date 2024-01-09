# Generated by Django 4.2 on 2023-12-22 21:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0005_project_invite_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="invite_link",
            field=models.CharField(
                blank=True,
                help_text="Максимально 150 символов",
                max_length=150,
                null=True,
                verbose_name="пригласительная ссылка",
            ),
        ),
    ]


__all__ = ()