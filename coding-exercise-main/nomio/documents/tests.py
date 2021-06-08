from datetime import date
from unittest import mock

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase

from .models import LegalDoc

class LegalDocModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="johnsmith", password="password")
        LegalDoc.objects.create(user=User.objects.get(id=1))
        LegalDoc.objects.create()
        
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

        # tests null=True
        test_legal_doc_no_user = LegalDoc.objects.get(id=2)
        self.assertEqual(test_legal_doc_no_user.user, None)


    def test_object_name(self):  # test __str__
        test_legal_doc = LegalDoc.objects.get(id=1)
        test_file = mock.MagicMock(spec=File)
        test_file.name = "test.pdf"
        test_legal_doc.doc = test_file
        expected_object_name = f"{test_legal_doc.doc.name} {test_legal_doc.user} {test_legal_doc.up_date}"
        self.assertEqual(expected_object_name, str(test_legal_doc))


