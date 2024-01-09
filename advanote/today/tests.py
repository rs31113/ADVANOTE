import django.contrib.auth
import django.test
import django.urls

import tasks.models
import users.models


class TodayViewTest(django.test.TestCase):
    def setUp(self):
        self.user = django.contrib.auth.get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        users.models.Profile.objects.create(user=self.user, email_confirm=True)

        tasks.models.Task.objects.create(title="Task 1", owner=self.user)
        tasks.models.Task.objects.create(
            title="Task 2",
            is_done=True,
            owner=self.user,
        )

        self.factory = django.test.RequestFactory()

    def test_today_view_with_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.get(django.urls.reverse("today:today"))

        self.assertEqual(response.status_code, 200)

        self.assertIn("tasks", response.context)
        self.assertIn("tasks_count", response.context)
        self.assertIn("tasks_with_status", response.context)

        tasks_list = response.context["tasks"]
        tasks_count = response.context["tasks_count"]
        tasks_with_status = response.context["tasks_with_status"]

        self.assertEqual(len(tasks_list), 2)
        self.assertEqual(tasks_count, 2)
        self.assertEqual(len(tasks_with_status), 2)


__all__ = ()
