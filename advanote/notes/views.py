import django.contrib.auth.mixins
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import django.views

import notes.forms
import notes.models


class GetNotes(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    def get(self, request):
        notes_list = notes.models.Note.objects.filter(
            owner=request.user,
        ).values("id", "title")
        return JsonResponse(list(notes_list), safe=False)


class Notes(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    def get(self, request):
        notes_list = notes.models.Note.objects.filter(owner=request.user)
        selected_note = None

        if notes_list:
            selected_note = notes_list[0]

        return render(
            request,
            "notes/hello.html",
            {"selected_note": selected_note, "notes": notes_list},
        )


class AddNote(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    model = notes.models.Note
    form_class = notes.forms.NoteForm
    template_name = "notes/add_note.html"
    success_url = "/notes/"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = notes.forms.NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()
            new_note_id = note.id
            return redirect("notes:edit_note", note_id=new_note_id)
        return render(request, self.template_name, {"form": form})


class EditNote(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    def get(self, request, note_id):
        selected_note = get_object_or_404(notes.models.Note, id=note_id)
        form = notes.forms.NoteForm(instance=selected_note)
        return render(
            request,
            "notes/notes.html",
            {"selected_note": selected_note, "form": form},
        )

    def post(self, request, note_id):
        selected_note = get_object_or_404(notes.models.Note, id=note_id)
        form = notes.forms.NoteForm(request.POST, instance=selected_note)
        if form.is_valid():
            form.save()
            return redirect("notes:notes")
        return render(
            request,
            "notes/notes.html",
            {"selected_note": selected_note, "form": form},
        )


class DeleteNote(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.View,
):
    def delete(self, request, note_id):
        note = get_object_or_404(notes.models.Note, id=note_id)
        note.delete()
        return JsonResponse({"message": "Заметка успешно удалена"})

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


__all__ = ()
