from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("authorization.urls", namespace="authorization")),
    path("today/", include("today.urls", namespace="today")),
    path("tasks/", include("tasks.urls", namespace="tasks")),
    path("notes/", include("notes.urls", namespace="notes")),
    path("projects/", include("projects.urls", namespace="projects")),
]
