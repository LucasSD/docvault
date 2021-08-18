from django.test import TestCase
from docvault.landing.forms import CustomUserCreationForm

class CustomUserCreationFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = CustomUserCreationForm()
        self.assertTrue(form.fields['email'])

    def test_form_valid(self):
        form = CustomUserCreationForm(data={'email': "lucas.stonedrake@gmail.com",
                                            "username": "lucas",
                                            "password1": "testpassword",
                                            "password2": "testpassword",
                                            })
        self.assertTrue(form.is_valid())

    def test_form_invalid_no_email(self):
        form = CustomUserCreationForm(data={"email": "",
                                            "username": "lucas",
                                            "password1": "testpassword",
                                            "password2": "testpassword",
                                            })
        self.assertFalse(form.is_valid())