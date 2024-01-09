import django.contrib.auth.models
import django.core.exceptions
import django.test
import django.urls

import tag.models
import tasks.forms
import tasks.models
import users.models


class CreateTaskTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = users.models.User.objects.create_user(
            "Max",
            "neverov@gmail.com",
            "123RTYdfd222",
        )
        cls.tag = tag.models.Tag.objects.create(
            name="Tag Test",
        )
        super().setUpClass()

    def test_create_task(self):
        tasks_count = tasks.models.Task.objects.count()
        tasks.models.Task.objects.create(
            owner=self.user,
            title="Test task",
            text="Task test text",
            priority=2,
        )
        self.assertEqual(tasks_count + 1, tasks.models.Task.objects.count())

    def test_task_priority(self):
        tasks.models.Task.objects.create(
            owner=self.user,
            title="Test task",
            text="Task test text",
            priority=2,
        )
        task = tasks.models.Task.objects.get(id=1)

        with self.subTest(task=task.priority):
            self.assertEqual(task.priority, 2)

    def test_task_title(self):
        tasks.models.Task.objects.create(
            owner=self.user,
            title="Test task",
            text="Task test text",
            priority=2,
        )
        task = tasks.models.Task.objects.get(id=1)

        with self.subTest(task=task.title):
            self.assertEqual(task.title, "Test task")

    def test_task_text(self):
        tasks.models.Task.objects.create(
            owner=self.user,
            title="Test task",
            text="Task test text",
            priority=2,
        )
        task = tasks.models.Task.objects.get(id=1)

        with self.subTest(task=task.text):
            self.assertEqual(task.text, "Task test text")

    def test_null_title_task(self):
        task = tasks.models.Task(
            owner=self.user,
            text="Task test text",
            priority=2,
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            task.full_clean()
            task.save()

    def test_null_text_task(self):
        task = tasks.models.Task(
            owner=self.user,
            title="Title))",
            priority=2,
        )
        task.full_clean()
        task.save()

    def test_task_with_tag(self):
        tasks.models.Task.objects.create(
            owner=self.user,
            title="Test task",
            text="Task test text",
            priority=2,
        )
        task = tasks.models.Task.objects.get(id=1)
        task.tags.add(self.tag)
        with self.subTest(task=task.tags.all()):
            self.assertEqual(task.tags.all().first(), self.tag)


class TaskViewsTestCase(django.test.TestCase):
    def setUp(self):
        self.user = django.contrib.auth.models.User.objects.create_user(
            username="testuser",
            password="testpass",
        )

        users.models.Profile.objects.create(
            user=self.user,
            email_confirm=False,
        )

        self.task = tasks.models.Task.objects.create(
            title="Test Task",
            text="Test task description",
            owner=self.user,
        )

    def test_delete_task_view(self):
        self.client.login(username="testuser", password="testpass")

        response = self.client.delete(
            django.urls.reverse("tasks:delete_task", args=[self.task.id]),
        )
        self.assertEqual(response.status_code, 302)

    def test_add_task_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(django.urls.reverse("tasks:add_task"))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            django.urls.reverse("tasks:add_task"),
            {
                "title": "New Task",
                "text": "New task description",
                "tags": [],
                "priority": 1,
            },
        )

        self.assertEqual(response.status_code, 302)

    def test_edit_task_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            django.urls.reverse("tasks:edit_task", args=[self.task.id]),
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            django.urls.reverse("tasks:edit_task", args=[self.task.id]),
            {
                "title": "Updated Task",
                "text": "Updated task description",
                "tags": [],
                "priority": 2,
            },
        )

        self.assertEqual(response.status_code, 302)


class TaskFormTestCase(django.test.TestCase):
    def test_task_form_valid_data(self):
        form_data = {
            "title": "Test Task",
            "text": "Test task description",
            "tags": [],
            "priority": 1,
        }
        form = tasks.forms.TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_blank_data(self):
        form_data = {}
        form = tasks.forms.TaskForm(data=form_data)
        self.assertFalse(form.is_valid())


class TaskModelTest(django.test.TestCase):
    def setUp(self):
        self.user = django.contrib.auth.models.User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.tag = tag.models.Tag.objects.create(name="Sample Tag")

        self.task = tasks.models.Task.objects.create(
            owner=self.user,
            title="Sample Task",
            text="This is a sample task.",
            priority=2,
            is_done=False,
        )
        self.task.tags.add(self.tag)

    def test_task_model_str_method(self):
        self.assertEqual(str(self.task), "Sample Task")

    def test_task_model_fields(self):
        self.assertEqual(self.task.title, "Sample Task")
        self.assertEqual(self.task.text, "This is a sample task.")
        self.assertEqual(self.task.priority, 2)
        self.assertFalse(self.task.is_done)
        self.assertEqual(self.task.tags.count(), 1)
        self.assertEqual(self.task.tags.first().name, "Sample Tag")
        self.assertEqual(self.task.owner, self.user)


__all__ = ()
