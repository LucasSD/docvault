from django.contrib.auth.models import User
from django.test import TestCase

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
