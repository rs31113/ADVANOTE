import django.urls

import projects.views

app_name = "projects"
urlpatterns = [
    django.urls.path(
        "create/",
        projects.views.AddProject.as_view(),
        name="create",
    ),
    django.urls.path(
        "delete_project/<int:project_id>/",
        projects.views.DeleteProject.as_view(),
        name="delete_project",
    ),
    django.urls.path(
        "",
        projects.views.ProjectsList.as_view(),
        name="page",
    ),
    django.urls.path(
        "edit/<int:project_id>/",
        projects.views.EditProject.as_view(),
        name="project_edit",
    ),
    django.urls.path(
        "<int:pk>/",
        projects.views.ProjectDetails.as_view(),
        name="project_detail",
    ),
    django.urls.path(
        "createlink/<int:pk>/",
        projects.views.CreateInviteLink.as_view(),
        name="create_invite",
    ),
    django.urls.path(
        "accept_invite/<int:pk>/<str:invite_code>/",
        projects.views.AcceptInvite.as_view(),
        name="invite_link",
    ),
]
