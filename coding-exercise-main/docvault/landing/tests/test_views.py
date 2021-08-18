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

class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="johnsmith", password="password", email = "another@email.com")

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/register.html")
        self.assertTemplateUsed(response, "landing/header.html")

    def test_form_post(self):

        form_entry = {
             "email": "test@email.com",
             "username": "lucas",
             "password1": "testpassword",
             "password2": "testpassword",                             
        }

        self.assertEqual(User.objects.count(), 1)
        response = self.client.post(reverse("register"), data=form_entry)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 2)

        test_user = User.objects.get(id=2)
        self.assertEqual(test_user.check_password("testpassword"), True)
        self.assertEqual("lucas", str(test_user.username))
        self.assertEqual("test@email.com", test_user.email)
        self.assertTrue(test_user.is_authenticated)


    def test_form_post_invalid_no_email(self):
        # one user from setup
        self.assertEqual(User.objects.count(), 1)

        form_entry = {
             "email": "",
             "username": "lucas",
             "password1": "testpassword",
             "password2": "testpassword",                             
        }

        response = self.client.post(reverse("register"), data=form_entry)
        self.assertEqual(response.status_code, 200)

        # check nothing added to database
        self.assertEqual(User.objects.count(), 1)


