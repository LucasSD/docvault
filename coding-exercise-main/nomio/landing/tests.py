from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class HomeTests(TestCase):
    def test_home_renders_on_get(self):
        response = self.client.get("")
        self.assertEqual(200, response.status_code)

    def test_home_logs_in_valid_user(self):
        User.objects.create_user(username="johnsmith", password="password")

        response = self.client.post(
            "", data={"username": "johnsmith", "password": "password"}
        )
        self.assertRedirects(response, "/documents/")

    def test_home_rejects_invalid_user(self):
        response = self.client.post(
            "", data={"username": "johnsmith", "password": "password"}
        )
        self.assertTrue(response.context["form"].errors)


class LogoutViewTests(TestCase):
    def test_view_url_accessible_by_name(self):
        self.client.login(username="johnsmith", password="password")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="johnsmith", password="password")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/home.html")
        self.assertTemplateUsed(response, "base.html")
