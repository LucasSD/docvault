from datetime import date
from unittest import mock

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from docvault.documents.models import LegalDoc, Tag


class LegalDocModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username="johnsmith", password="password")
        LegalDoc.objects.create(user=test_user)
        cls.test_legaldoc = LegalDoc.objects.get(id=1)
        cls.mock_file = mock.MagicMock(spec=File)
        cls.mock_file.name = "test.pdf"

    def test_doc_field(self):

        # TODO: Add to doc field when test_legaldoc created
        # (this creates different mock file names which I am yet to resolve).
        # If resolved, the line below will be redundant.
        self.test_legaldoc.doc = self.mock_file
        self.assertEqual(self.test_legaldoc.doc.name, "test.pdf")
        self.assertEqual(self.test_legaldoc.doc.url, "/media/test.pdf")

    def test_up_date_field(self):
        self.assertEqual(self.test_legaldoc.up_date, date.today())

    def test_user_field(self):
        self.assertEqual(str(self.test_legaldoc.user), "johnsmith")

    def test_tag_field(self):
        test_tag = Tag.objects.create(name="some_category")
        self.test_legaldoc.tag.add(test_tag)
        self.test_legaldoc.save()

        expected_tag = str(
            self.test_legaldoc.tag.all()[0]
        )  # queryset is a list of length one
        self.assertEqual(expected_tag, "some_category")

    def test_obj_name(self):  # test __str__
        self.test_legaldoc.doc = self.mock_file
        expected_obj_name = f"{self.test_legaldoc.doc.name} {self.test_legaldoc.user} {self.test_legaldoc.up_date}"
        self.assertEqual(expected_obj_name, str(self.test_legaldoc))


class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_tag = Tag.objects.create(name="some_category")

    def test_name_field(self):
        self.assertEqual(self.test_tag.name, "some_category")
        max_length = self.test_tag._meta.get_field("name").max_length
        self.assertEqual(max_length, 80)

    def test_obj_name(self):  # test __str__
        expected_obj_name = f"{self.test_tag.name}"
        self.assertEqual(expected_obj_name, "some_category")
