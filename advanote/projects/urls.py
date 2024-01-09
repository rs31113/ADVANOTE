import django.urls

import projects.views

app_name = "projects"
urlpatterns = [
    django.urls.path(
        "create/",
        projects.views.CreateProject.as_view(),
        name="create",
    ),
    django.urls.path(
        "",
        projects.views.ProjectsListPage.as_view(),
        name="page",
    ),
    django.urls.path(
        "edite/<int:project_id>/",
        projects.views.ProjectEditPage.as_view(),
        name="project_edite",
    ),
    django.urls.path(
        "<int:pk>/",
        projects.views.ProjectDetail.as_view(),
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
