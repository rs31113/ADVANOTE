import uuid

import django.contrib.auth.mixins
import django.http
import django.shortcuts
import django.urls
import django.views.generic

import projects.forms
import projects.models


class CreateProject(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.FormView,
):
    form_class = projects.forms.ProjectCreateForm
    success_url = django.urls.reverse_lazy("projects:page")
    template_name = "projects/create.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(request)
        context = {
            "form": form,
        }
        return django.shortcuts.render(request, self.template_name, context)

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


class ProjectsListPage(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.ListView,
):
    context_object_name = "projects"
    template_name = "projects/projects_page.html"

    def get_queryset(self):
        return projects.models.Project.objects.get_all_user_projects(
            self.request.user,
        )


class ProjectEditPage(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.views.generic.View,
):
    template_name = "projects/project_edite.html"

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
        return django.shortcuts.render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        project = projects.models.Project.objects.get(id=kwargs["project_id"])
        form = projects.forms.ProjectPageEditForm(instance=project)
        context = {
            "form": form,
            "project": project,
        }
        return django.shortcuts.render(request, self.template_name, context)


class ProjectDetail(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.views.generic.DetailView,
):
    model = projects.models.Project
    template_name = "projects/project.html"

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
        project = django.shortcuts.get_object_or_404(
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
            return django.shortcuts.redirect(
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
        project = django.shortcuts.get_object_or_404(
            projects.models.Project,
            pk=kwargs["pk"],
        )
        if request.user == project.owner:
            project.invite_link = uuid.uuid4()
            project.save()
        return django.shortcuts.redirect(
            django.urls.reverse(
                "projects:project_detail",
                kwargs={"pk": kwargs["pk"]},
            ),
        )


__all__ = ()
