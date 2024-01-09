from django.urls import path

import notes.views


app_name = "notes"
urlpatterns = [
    path("", notes.views.Notes.as_view(), name="notes"),
    path("add_note/", notes.views.AddNote.as_view(), name="add_note"),
    path("<int:note_id>/", notes.views.EditNote.as_view(), name="edit_note"),
    path(
        "<int:note_id>/delete/",
        notes.views.DeleteNote.as_view(),
        name="delete_note",
    ),
    path("get_notes/", notes.views.GetNotes.as_view(), name="get_notes"),
]
