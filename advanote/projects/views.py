import uuid

import django.contrib.auth.mixins
import django.http
from django.shortcuts import get_object_or_404, redirect, render
import django.urls
import django.views.generic

import projects.forms
import projects.models


class AddProject(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.FormView,
):
    form_class = projects.forms.ProjectCreateForm
    success_url = django.urls.reverse_lazy("projects:page")
    template_name = "projects/add_project.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(request)
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)

    def get_form(self, form_class=None, **kwargs):
        if form_class is None:
            form_class = self.get_form_class()
        params = self.get_form_kwargs()
        params.update(kwargs)
        return form_class(**params)

    def post(self, request, *args, **kwargs):
        form = self.get_form(request=request)
        if form.is_valid():
            return self.form_valid(form, request=request)
        return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form, **kwargs):
        project = form.save(commit=False)
        project.owner = kwargs["request"].user
        project.save()
        form.save_m2m()
        return super().form_valid(form)


class ProjectsList(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.ListView,
):
    context_object_name = "projects"
    template_name = "projects/projects.html"

    def get_queryset(self):
        return projects.models.Project.objects.get_all_user_projects(
            self.request.user,
        )


class EditProject(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.views.generic.View,
):
    template_name = "projects/edit_project.html"

    def test_func(self):
        project = projects.models.Project.objects.get_all_members(
            self.kwargs["project_id"],
        )
        if not project.exists():
            return False
        project = project[0]
        if project.owner == self.request.user:
            return True
        if self.request.user in project.members.all():
            return True
        return False

    def post(self, request, *args, **kwargs):
        project = projects.models.Project.objects.get(id=kwargs["project_id"])
        form = projects.forms.ProjectPageEditForm(
            request.POST,
            instance=project,
        )

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()

        context = {
            "form": form,
            "project": project,
        }
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        project = projects.models.Project.objects.get(id=kwargs["project_id"])
        form = projects.forms.ProjectPageEditForm(instance=project)
        context = {
            "form": form,
            "project": project,
        }
        return render(request, self.template_name, context)


class DeleteProject(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    def delete(self, request, project_id):
        project = get_object_or_404(projects.models.Project, id=project_id)
        project.delete()
        return django.http.JsonResponse({"message": "Project deleted successfully"})

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProjectDetails(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.views.generic.DetailView,
):
    model = projects.models.Project
    template_name = "projects/project_details.html"

    def test_func(self):
        project = projects.models.Project.objects.get_all_members(
            self.kwargs["pk"],
        )
        if not project.exists():
            return False
        project = project[0]
        if project.owner == self.request.user:
            return True
        if self.request.user in project.members.all():
            return True
        return False


class AcceptInvite(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.View,
):
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(
            projects.models.Project,
            pk=kwargs["pk"],
        )
        if all(
            (
                project.invite_link == kwargs["invite_code"],
                request.user not in project.members.all(),
                request.user != project.owner,
            ),
        ):
            project.members.add(request.user)
            return redirect(
                django.urls.reverse(
                    "projects:project_detail",
                    kwargs={"pk": kwargs["pk"]},
                ),
            )
        return django.http.HttpResponse(
            "Ссылка не действительна или вы уже приняли приглашение!",
        )


class CreateInviteLink(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.View,
):
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(
            projects.models.Project,
            pk=kwargs["pk"],
        )
        if request.user == project.owner:
            project.invite_link = uuid.uuid4()
            project.save()
        return redirect(
            django.urls.reverse(
                "projects:project_detail",
                kwargs={"pk": kwargs["pk"]},
            ),
        )


__all__ = ()
