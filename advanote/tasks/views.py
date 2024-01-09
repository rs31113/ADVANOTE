import json

import django.contrib.auth.mixins
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import django.views

import tasks.forms
import tasks.models


class AddTask(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    model = tasks.models.Task
    form_class = tasks.forms.TaskForm
    template_name = "tasks/add_task.html"
    success_url = "/today/"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = tasks.forms.TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect("today:today")
        return render(request, self.template_name, {"form": form})


class EditTask(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    def get(self, request, task_id):
        task = get_object_or_404(tasks.models.Task, id=task_id)
        form = tasks.forms.TaskForm(instance=task)
        return render(
            request,
            "tasks/edit_task.html",
            {"form": form, "task": task},
        )

    def post(self, request, task_id):
        task = get_object_or_404(tasks.models.Task, id=task_id)
        form = tasks.forms.TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("today:today")
        return render(
            request,
            "tasks/edit_task.html",
            {"form": form, "task": task},
        )


class DeleteTask(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    def delete(self, request, task_id):
        task = get_object_or_404(tasks.models.Task, id=task_id)
        task.delete()
        return JsonResponse({"message": "Task deleted successfully"})

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UpdateTaskStatus(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    def post(self, request, task_id):
        task = tasks.models.Task.objects.get(id=task_id)
        data = json.loads(request.body)
        is_done = data.get("isDone")
        if is_done is not None:
            task.is_done = is_done
            task.save()

            return JsonResponse({"status": "success"})

        return JsonResponse(
            {"status": "failure", "error": "Invalid request data"},
        )


__all__ = ()
