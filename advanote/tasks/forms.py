import django.forms

import tasks.models


class TaskForm(django.forms.ModelForm):
    class Meta:
        model = tasks.models.Task
        fields = ["title", "text", "tags", "priority"]
        widgets = {
            "title": django.forms.TextInput(
                attrs={"placeholder": "Заголовок"},
            ),
            "text": django.forms.Textarea(
                attrs={"placeholder": "Описание"},
            ),
        }


__all__ = ()
