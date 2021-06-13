from datetime import date
from unittest import mock

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.urls import reverse

from .models import LegalDoc


class LegalDocModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="johnsmith", password="password")
        LegalDoc.objects.create(user=User.objects.get(id=1))

    def setUp(self):
        self.test_legaldoc = LegalDoc.objects.get(id=1)

        # use mocks instead of file system
        self.mock_file = mock.MagicMock(spec=File)
        self.mock_file.name = "test.pdf"

    def test_up_date_field(self):
        self.assertEqual(self.test_legaldoc.up_date, date.today())

    def test_doc_field(self):
        # TODO: Add to doc field when test_legaldoc created 
        # (this creates different mock file names which I am yet to resolve).
        # If resolved, the line below will be redundant.
        self.test_legaldoc.doc = self.mock_file
        self.assertEqual(self.test_legaldoc.doc.name, self.mock_file.name)
        self.assertEqual(self.test_legaldoc.doc.url, "/media/test.pdf")

    def test_user_field(self): 
        self.assertEqual(str(self.test_legaldoc.user), "johnsmith")

    def test_obj_name(self):  # test __str__
        self.test_legaldoc.doc = self.mock_file
        expected_obj_name = f"{self.test_legaldoc.doc.name} {self.test_legaldoc.user} {self.test_legaldoc.up_date}"
        self.assertEqual(expected_obj_name, str(self.test_legaldoc))


class LegalDocListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="johnsmith", password="password")
        mock_file_pdf = mock.MagicMock(spec=File)
        mock_file_pdf.name = "test.pdf"
        mock_file_pdf.read.return_value = "fakecontents"
        mock_file_jpg = mock.MagicMock(spec=File)
        mock_file_jpg.name = "test.jpg"
        mock_file_jpg.read.return_value = "fakecontents"
        LegalDoc.objects.create(doc=mock_file_pdf, user=User.objects.get(id=1))
        for i in range(9):
            LegalDoc.objects.create(doc=mock_file_jpg, user=User.objects.get(id=1))

    def setUp(self):
        self.client.force_login(User.objects.get(id=1))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("index"))
        self.assertRedirects(response, "/?next=/documents/")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/documents/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "documents/legaldoc_list.html")
        self.assertTemplateUsed(response, "base.html")

    def test_pagination_is_eight(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["legaldoc_list"]), 8)

    def test_lists_all_legaldocs(self):
        # Get second page and confirm it has (exactly) 2 remaining objects
        response = self.client.get(reverse("index") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["legaldoc_list"]), 2)

    def test_context(self):
        response1 = self.client.get(reverse("index"))
        self.assertEqual(response1.status_code, 200)
        test_legaldoc1 = response1.context["legaldoc_list"][0]
        test_legaldoc2 = response1.context["legaldoc_list"][1]
        self.assertEqual(date.today(), test_legaldoc1.up_date)
        self.assertEqual("johnsmith", str(test_legaldoc1.user))
        self.assertEqual("test.pdf", test_legaldoc1.doc.name)
        self.assertEqual("test.jpg", test_legaldoc2.doc.name)
        response2 = self.client.get(reverse("index") + "?page=2")
        self.assertEqual(response2.status_code, 200)
        test_legaldoc = response2.context["legaldoc_list"][0]
        self.assertEqual("johnsmith", str(test_legaldoc.user))
        self.assertEqual(date.today(), test_legaldoc.up_date)


class UploadViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="johnsmith", password="password")

    def setUp(self):
        self.client.force_login(User.objects.get(id=1))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("upload"))
        self.assertRedirects(response, "/?next=/documents/upload/")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/documents/upload/")
        self.assertEqual(str(response.context["user"]), "johnsmith")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("upload"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("upload"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "documents/user_upload.html")
        self.assertTemplateUsed(response, "base.html")

    def test_initial_form_context(self):
        response = self.client.get(reverse("upload"))
        self.assertEqual(response.status_code, 200)

        test_form = response.context["form"]
        self.assertIn("form", response.context)
        self.assertEqual({}, test_form.initial)

    def test_form_post(self):
        mock_file = mock.MagicMock(spec=File)
        mock_file.name = "test.img"

        form_entry = {
            "doc": mock_file,
        }

        response = self.client.post(reverse("upload"), data=form_entry)
        self.assertEqual(response.status_code, 200)
        test_legaldoc = LegalDoc.objects.get(id=1)
        self.assertEqual(LegalDoc.objects.count(), 1)
        self.assertEqual(mock_file.name, test_legaldoc.doc.name)
        self.assertEqual(date.today(), test_legaldoc.up_date)
        self.assertEqual("johnsmith", str(test_legaldoc.user))
