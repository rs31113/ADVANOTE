import django.contrib.auth.models
import django.test
import django.urls

import users.forms
import users.models


class FormsTest(django.test.TestCase):
    def test_signup_form_valid_data(self):
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        form = users.forms.SingUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_change_form_valid_data(self):
        form_data = {
            "old_password": "oldpassword",
            "new_password1": "NewP@ssw0rd",
            "new_password2": "NewP@ssw0rd",
        }
        user = django.contrib.auth.models.User.objects.create_user(
            username="testuser",
            password="oldpassword",
        )
        form = users.forms.PasswordChangeForm(user=user, data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_user_change_form_valid_data(self):
        form_data = {
            "username": "newusername",
            "first_name": "New",
            "last_name": "User",
        }
        form = users.forms.UserChangeForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewsTest(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()
        self.user = django.contrib.auth.models.User.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        users.models.Profile.objects.create(user=self.user)

    def test_profile_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            django.urls.reverse("authorization:profile"),
        )
        self.assertEqual(response.status_code, 302)


class ModelsTest(django.test.TestCase):
    def test_create_user(self):
        user = django.contrib.auth.models.User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        self.assertIsInstance(user, django.contrib.auth.models.User)

    def test_create_profile(self):
        user = django.contrib.auth.models.User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        profile = users.models.Profile.objects.create(
            user=user,
            birthday="2000-01-01",
        )
        self.assertIsInstance(profile, users.models.Profile)


__all__ = ()
