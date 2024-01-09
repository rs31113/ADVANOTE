import django.contrib.auth.mixins
from django.shortcuts import render
import django.views

import tasks.models


class Today(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.TemplateView,
):
    template_name = "today/today.html"

    def get(self, request, *args, **kwargs):
        tasks_list = tasks.models.Task.objects.all()
        tasks_count = tasks_list.count()
        tasks_with_status = [(task, task.is_done) for task in tasks_list]
        return render(
            request,
            self.template_name,
            {
                "tasks": tasks_list,
                "tasks_count": tasks_count,
                "tasks_with_status": tasks_with_status,
            },
        )


__all__ = ()
