from datetime import date
from unittest import mock

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.urls import reverse
from docvault.documents.models import LegalDoc, Tag


class LegalDocListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="johnsmith", password="password")
        test_tag1 = Tag.objects.create(name="some_category")
        test_tag2 = Tag.objects.create(name="any_category")

        mock_file_pdf = mock.MagicMock(spec=File)
        mock_file_pdf.name = "test.pdf"

        # avoid TypeError on f.write
        mock_file_pdf.read.return_value = "fakecontents"

        mock_file_jpg = mock.MagicMock(spec=File)
        mock_file_jpg.name = "test.jpg"

        # avoid TypeError on f.write
        mock_file_jpg.read.return_value = "fakecontents"

        # add first LegalDoc
        LegalDoc.objects.create(doc=mock_file_pdf, user=test_user)
        for i in range(9):
            # add nine LegalDocs
            LegalDoc.objects.create(doc=mock_file_jpg, user=test_user)

        # add to M2M fields directly
        for i in range(1, 11):
            _ = LegalDoc.objects.get(id=i)
            _.tag.add(test_tag1, test_tag2)
            _.save()

    def setUp(self):
        self.client.force_login(User.objects.get(id=1))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("index"))
        self.assertRedirects(response, "/?next=/documents/")

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/documents/")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
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
        # Confirm second page has two remaining objects
        response = self.client.get(reverse("index") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["legaldoc_list"]), 2)

    # some of these tests may be redundant
    def test_context(self):
        # page 1
        response1 = self.client.get(reverse("index"))
        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, "doc")

        test_legaldoc1 = response1.context["legaldoc_list"][0]
        self.assertEqual(date.today(), test_legaldoc1.up_date)
        self.assertEqual("johnsmith", str(test_legaldoc1.user))
        self.assertEqual("test.pdf", test_legaldoc1.doc.name)
        self.assertEqual("some_category, any_category", test_legaldoc1.display_tag())

        test_legaldoc2 = response1.context["legaldoc_list"][1]
        self.assertEqual("test.jpg", test_legaldoc2.doc.name)
        self.assertEqual("some_category, any_category", test_legaldoc2.display_tag())

        # page 2
        response2 = self.client.get(reverse("index") + "?page=2")
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, "doc")

        test_legaldoc = response2.context["legaldoc_list"][0]
        self.assertEqual(date.today(), test_legaldoc.up_date)
        self.assertEqual("johnsmith", str(test_legaldoc.user))
        self.assertEqual("test.jpg", test_legaldoc2.doc.name)
        self.assertEqual("some_category, any_category", test_legaldoc.display_tag())


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

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/documents/upload/")
        self.assertEqual(str(response.context["user"]), "johnsmith")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("upload"))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
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

        test_tag1 = Tag(name="XXX")
        test_tag1.save()
        test_tag1 = Tag.objects.get(id=1)

        form_entry = {
            "doc": mock_file,
            "Tag": test_tag1,  # this may not be correct
        }

        self.assertEqual(LegalDoc.objects.count(), 0)
        response = self.client.post(reverse("upload"), data=form_entry)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LegalDoc.objects.count(), 1)

        test_legaldoc = LegalDoc.objects.get(id=1)
        self.assertEqual(date.today(), test_legaldoc.up_date)
        self.assertEqual("johnsmith", str(test_legaldoc.user))
        self.assertEqual("test.img", test_legaldoc.doc.name)
        # self.assertEqual("test.img", test_legaldoc.tag.all()) alway empty queryset

    def test_form_post_file_invalid(self):
        mock_file = mock.MagicMock(spec=File)
        mock_file.name = "test.html"

        form_entry = {
            "doc": mock_file,
        }

        response = self.client.post(reverse("upload"), data=form_entry)
        self.assertEqual(response.status_code, 200)

        # check nothing added to database
        self.assertEqual(LegalDoc.objects.count(), 0)

    def test_form_post_multiple_files(self):
        mock_file1 = mock.MagicMock(spec=File)
        mock_file1.name = "test.xxx"

        mock_file2 = mock.MagicMock(spec=File)
        mock_file2.name = "test2.img"

        form_entry = {"doc": (mock_file1, mock_file2)}

        self.assertEqual(LegalDoc.objects.count(), 0)
        response = self.client.post(reverse("upload"), data=form_entry)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LegalDoc.objects.count(), 2)


class LegalDocDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="johnsmith", password="password")
        mock_file_png = mock.MagicMock(spec=File)
        mock_file_png.name = "test.png"

        # avoid TypeError on f.write
        mock_file_png.read.return_value = "fakecontents"

        mock_file_txt = mock.MagicMock(spec=File)
        mock_file_txt.name = "test.txt"

        # avoid TypeError on f.write
        mock_file_txt.read.return_value = "fakecontents"

        # add one PNG and 3 .txt files to database
        LegalDoc.objects.create(doc=mock_file_png, user=test_user)
        for i in range(3):
            LegalDoc.objects.create(doc=mock_file_txt, user=test_user)

        cls.test_legaldoc = LegalDoc.objects.get(id=1)

    def setUp(self):
        self.client.force_login(User.objects.get(id=1))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse("delete", kwargs={"pk": self.test_legaldoc.id}),
        )
        self.assertRedirects(response, "/?next=/documents/delete/1")

    def test_url_post(self):
        response = self.client.post(
            reverse("delete", kwargs={"pk": self.test_legaldoc.id})
        )
        self.assertRedirects(response, "/documents/")

    def test_uses_correct_template(self):
        response = self.client.get(
            reverse("delete", kwargs={"pk": self.test_legaldoc.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "documents/legaldoc_confirm_delete.html")
        self.assertTemplateUsed(response, "base.html")

    def test_file_deleted(self):
        self.assertEqual(LegalDoc.objects.count(), 4)
        response = self.client.post(
            reverse("delete", kwargs={"pk": self.test_legaldoc.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LegalDoc.objects.count(), 3)

        # test instance with id=1 is deleted
        self.assertFalse(LegalDoc.objects.filter(id=1))
