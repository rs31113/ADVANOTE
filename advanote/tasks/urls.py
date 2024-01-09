from django.urls import path

import tasks.views


app_name = "tasks"
urlpatterns = [
    path(
        "add_task/",
        tasks.views.AddTask.as_view(),
        name="add_task",
    ),
    path(
        "edit_task/<int:task_id>/",
        tasks.views.EditTask.as_view(),
        name="edit_task",
    ),
    path(
        "delete_task/<int:task_id>/",
        tasks.views.DeleteTask.as_view(),
        name="delete_task",
    ),
    path(
        "update_task_status/<int:task_id>/",
        tasks.views.UpdateTaskStatus.as_view(),
        name="update_task_status",
    ),
]


__all__ = ()
