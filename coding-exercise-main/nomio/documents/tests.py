from datetime import date
from unittest import mock
from unittest.case import addModuleCleanup

from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase

from .models import LegalDoc
from .forms import UserUploadForm


class LegalDocModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="johnsmith", password="password")
        LegalDoc.objects.create(user=User.objects.get(id=1))

    def test_up_date_field(self):
        test_legal_doc = LegalDoc.objects.get(id=1)
        self.assertEqual(test_legal_doc.up_date, date.today())

    def test_doc_field(self):
        test_file = mock.MagicMock(spec=File)
        test_file.name = "test.pdf"
        test_legal_doc = LegalDoc.objects.get(id=1)
        test_legal_doc.doc = test_file
        self.assertEqual(test_legal_doc.doc.name, test_file.name)
        self.assertEqual(test_legal_doc.doc.url, "/media/test.pdf")

    def test_user_field(self):  # test ForeignKey Field
        test_legal_doc = LegalDoc.objects.get(id=1)
        self.assertEqual(str(test_legal_doc.user), "johnsmith")

    def test_object_name(self):  # test __str__
        test_legal_doc = LegalDoc.objects.get(id=1)
        test_file = mock.MagicMock(spec=File)
        test_file.name = "test.pdf"
        test_legal_doc.doc = test_file
        expected_object_name = (
            f"{test_legal_doc.doc.name} {test_legal_doc.user} {test_legal_doc.up_date}"
        )
        self.assertEqual(expected_object_name, str(test_legal_doc))


class LegalDocListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="johnsmith", password="password")
        test_file_pdf = mock.MagicMock(spec=File)
        test_file_pdf.name = "test.pdf"
        test_file_pdf.read.return_value = "fakecontents"
        test_file_jpg = mock.MagicMock(spec=File)
        test_file_jpg.name = "test.jpg"
        test_file_jpg.read.return_value = "fakecontents"
        LegalDoc.objects.create(doc=test_file_pdf, user=User.objects.get(id=1))
        for i in range(9):
            LegalDoc.objects.create(doc=test_file_jpg, user=User.objects.get(id=1))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("index"))
        self.assertRedirects(response, "/?next=/documents/")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="johnsmith", password="password")
        response = self.client.get("/documents/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="johnsmith", password="password")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="johnsmith", password="password")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "documents/legaldoc_list.html")
        self.assertTemplateUsed(response, "base.html")

    def test_pagination_is_eight(self):
        self.client.login(username="johnsmith", password="password")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["legaldoc_list"]), 8)

    def test_lists_all_legaldocs(self):
        # Get second page and confirm it has (exactly) 2 remaining objects
        self.client.login(username="johnsmith", password="password")
        response = self.client.get(reverse("index") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["legaldoc_list"]), 2)

    def test_context(self):
        self.client.login(username="johnsmith", password="password")
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

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("upload"))
        self.assertRedirects(response, "/?next=/documents/upload/")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="johnsmith", password="password")
        response = self.client.get("/documents/upload/")
        self.assertEqual(str(response.context["user"]), "johnsmith")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="johnsmith", password="password")
        response = self.client.get(reverse("upload"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="johnsmith", password="password")
        response = self.client.get(reverse("upload"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "documents/user_upload.html")
        self.assertTemplateUsed(response, "base.html")

    def test_initial_form_context(self):
        self.client.login(username="johnsmith", password="password")
        response = self.client.get(reverse("upload"))
        self.assertEqual(response.status_code, 200)

        test_form = response.context["form"]
        self.assertIn("form", response.context)
        self.assertEqual({}, test_form.initial)

    def test_form_post(self):
        self.client.login(username="johnsmith", password="password")
        test_file = mock.MagicMock(spec=File)
        test_file.name = "test.img"

        form_entry = {
            "doc": test_file,
        }

        response = self.client.post(reverse("upload"), data=form_entry)
        self.assertEqual(response.status_code, 200)
        test_legaldoc = LegalDoc.objects.get(id=1)
        self.assertEqual(LegalDoc.objects.count(), 1)
        self.assertEqual(test_file.name, test_legaldoc.doc.name)
        self.assertEqual(date.today(), test_legaldoc.up_date)
        self.assertEqual("johnsmith", str(test_legaldoc.user))
