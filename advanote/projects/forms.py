import django.forms

import notes.models
import projects.models
import tasks.models


class ProjectCreateForm(django.forms.ModelForm):
    task = django.forms.ModelMultipleChoiceField(
        queryset=None,
        widget=django.forms.CheckboxSelectMultiple(),
        required=False,
    )
    note = django.forms.ModelMultipleChoiceField(
        queryset=None,
        widget=django.forms.CheckboxSelectMultiple(),
        required=False,
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            "task"
        ].queryset = tasks.models.Task.objects.get_user_tasks(
            request.user.id,
        )
        self.fields[
            "note"
        ].queryset = notes.models.Note.objects.get_user_notes(
            request.user.id,
        )

    class Meta:
        model = projects.models.Project
        fields = (
            projects.models.Project.name.field.name,
            projects.models.Project.description.field.name,
            projects.models.Project.task.field.name,
            projects.models.Project.note.field.name,
        )


class ProjectPageEditForm(django.forms.ModelForm):
    task = django.forms.ModelMultipleChoiceField(
        queryset=None,
        widget=django.forms.CheckboxSelectMultiple(),
        required=False,
    )
    note = django.forms.ModelMultipleChoiceField(
        queryset=None,
        widget=django.forms.CheckboxSelectMultiple(),
        required=False,
    )
    members = django.forms.ModelMultipleChoiceField(
        queryset=None,
        widget=django.forms.CheckboxSelectMultiple(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].queryset = self.instance.task
        self.fields["note"].queryset = self.instance.note
        self.fields["members"].queryset = self.instance.members

    class Meta:
        model = projects.models.Project
        fields = (
            projects.models.Project.name.field.name,
            projects.models.Project.description.field.name,
            projects.models.Project.members.field.name,
            projects.models.Project.task.field.name,
            projects.models.Project.note.field.name,
        )


__all__ = ()
