from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class HomeTest(TestCase):
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


class LogoutViewTest(TestCase):
    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/home.html")
        self.assertTemplateUsed(response, "base.html")

class PasswordChangeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="johnsmith", password="password")

    def setUp(self):
        # log user in to avoid redirects
        self.client.force_login(User.objects.get(id=1))

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/accounts/password_change/")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("password_change"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("password_change"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/password_change_form.html")
        self.assertTemplateUsed(response, "base.html")

class PasswordChangeDoneViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="johnsmith", password="password")

    def setUp(self):
        # log user in to avoid redirects
        self.client.force_login(User.objects.get(id=1))

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/accounts/password_change/done/")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("password_change_done"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("password_change_done"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/password_change_done.html")
        self.assertTemplateUsed(response, "base.html")

class PasswordResetViewTest(TestCase):
    def test_url_exists_at_desired_location(self):
        response = self.client.get("/accounts/password_reset/")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/password_reset_form.html")
        self.assertTemplateUsed(response, "base.html")

class PasswordResetDoneViewTest(TestCase):
    def test_url_exists_at_desired_location(self):
        response = self.client.get("/accounts/password_reset/done/")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("password_reset_done"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("password_reset_done"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/password_reset_done.html")
        self.assertTemplateUsed(response, "base.html")

'''class PasswordResetConfirmViewTest(TestCase):
    def test_url_exists_at_desired_location(self):
        response = self.client.get("accounts/reset/<uidb64>/<token>/")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("password_reset_confirm"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("password_reset_confirm"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/password_reset_confirm.html")
        self.assertTemplateUsed(response, "base.html")'''

class PasswordResetCompleteViewTest(TestCase):
    def test_url_exists_at_desired_location(self):
        response = self.client.get("/accounts/reset/done")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("password_reset_complete"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("password_reset_complete"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/password_reset_complete.html")
        self.assertTemplateUsed(response, "base.html")
