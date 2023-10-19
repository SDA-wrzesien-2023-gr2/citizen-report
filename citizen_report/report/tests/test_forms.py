from django.contrib.auth import get_user_model
from django.test import TestCase

from ..constants import Category, Status
from ..forms import ReportForm, UpdateReportForm

User = get_user_model()


class FormReportTest(TestCase):
    def setUp(self):
        self.data = {'title': 'Test form', 'text': 'Text test', 'category': Category.POWER_SUPPLY}
        self.invalid_data = {'title': '', 'text': 'Text test', 'category': ''}

    def test_form_report(self):
        form = ReportForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = ReportForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())


class FormUpdateReportTest(TestCase):
    def setUp(self):
        self.data = {'status': Status.CHECKING}
        self.invalid_data = {'status': ''}

    def test_update_form_report(self):
        form = UpdateReportForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = ReportForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())