import django.test

import notes.models
import projects.models
import tasks.models
import users.models


class CreateProjectTests(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = users.models.User.objects.create_user(
            "Max1112",
            "n12everov@gmail.com",
            "123RTYdfd222",
        )
        cls.member = users.models.User.objects.create_user(
            "Max",
            "neverov@gmail.com",
            "123RTYdfd222",
        )
        cls.member1 = users.models.User.objects.create_user(
            "Max2",
            "neve1rov@gmail.com",
            "123RTYdfd222",
        )
        cls.note = notes.models.Note(
            title="Title!",
            owner=cls.user,
            text="Test text!",
        )
        cls.note.full_clean()
        cls.note.save()
        cls.note1 = notes.models.Note(
            title="Title!",
            owner=cls.user,
            text="Test text!",
        )
        cls.note1.full_clean()
        cls.note1.save()
        cls.task = tasks.models.Task(
            owner=cls.user,
            title="Test task",
            text="Task test text",
            priority=2,
        )
        cls.task.full_clean()
        cls.task.save()
        cls.task1 = tasks.models.Task(
            owner=cls.user,
            title="Test task",
            text="Task test text",
            priority=2,
        )
        cls.task1.full_clean()
        cls.task1.save()
        super().setUpTestData()

    def test_create_project(self):
        project_count = projects.models.Project.objects.count()
        project = projects.models.Project(
            owner=self.user,
            name="Project",
        )
        project.full_clean()
        project.save()
        self.assertEqual(
            project_count + 1,
            projects.models.Project.objects.count(),
        )

    def test_add_member_project(self):
        project = projects.models.Project.objects.create(
            owner=self.user,
            name="Project",
        )
        project.members.add(self.member)
        project.members.add(self.member1)
        project.full_clean()
        project.save()
        self.assertEqual(project.members.first(), self.member)
        self.assertEqual(project.members.all()[1], self.member1)

    def test_add_note_project(self):
        project = projects.models.Project.objects.create(
            owner=self.user,
            name="Project",
        )
        project.note.add(self.note)
        project.note.add(self.note1)
        project.full_clean()
        project.save()
        self.assertEqual(project.note.first(), self.note)
        self.assertEqual(project.note.all()[1], self.note1)

    def test_add_task_project(self):
        project = projects.models.Project.objects.create(
            owner=self.user,
            name="Project",
        )
        project.task.add(self.task)
        project.task.add(self.task1)
        project.full_clean()
        project.save()
        self.assertEqual(project.task.first(), self.task)
        self.assertEqual(project.task.all()[1], self.task1)

    def test_full_project(self):
        project = projects.models.Project.objects.create(
            owner=self.user,
            name="Advanote",
        )
        project.members.add(self.member)
        project.members.add(self.member1)
        project.note.add(self.note)
        project.note.add(self.note1)
        project.task.add(self.task)
        project.task.add(self.task1)
        project.full_clean()
        project.save()
        self.assertEqual(project.members.first(), self.member)
        self.assertEqual(project.members.all()[1], self.member1)
        self.assertEqual(project.note.first(), self.note)
        self.assertEqual(project.note.all()[1], self.note1)
        self.assertEqual(project.task.first(), self.task)
        self.assertEqual(project.task.all()[1], self.task1)


__all__ = ()
