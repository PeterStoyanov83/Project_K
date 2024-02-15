from django.test import TestCase
from clients.forms import ClientFileForm, ResourceForm, LaptopForm
from clients.models import ClientFile, Resource, Laptop

class ClientFileFormTest(TestCase):
    def test_valid_form(self):
        # Create a file instance
        file_data = {'file': 'test.txt'}
        form = ClientFileForm(data=file_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test with empty data
        form = ClientFileForm(data={})
        self.assertFalse(form.is_valid())


class ResourceFormTest(TestCase):
    def test_valid_form(self):
        # Create a resource instance
        resource_data = {'seat_number': 1, 'course': None, 'client': None}
        form = ResourceForm(data=resource_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test with empty data
        form = ResourceForm(data={})
        self.assertFalse(form.is_valid())

    def test_optional_seat_number(self):
        # Test that seat_number is optional
        form = ResourceForm(data={'course': None, 'client': None})
        self.assertTrue(form.is_valid())


class LaptopFormTest(TestCase):
    def test_valid_form(self):
        # Create a laptop instance
        laptop_data = {'name': 'Test Laptop', 'assigned_to': None, 'period_start': '2024-01-01', 'period_end': '2024-01-30'}
        form = LaptopForm(data=laptop_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Test with empty data
        form = LaptopForm(data={})
        self.assertFalse(form.is_valid())

    def test_period_end_before_start(self):
        # Test validation when period_end is before period_start
        laptop_data = {'name': 'Test Laptop', 'assigned_to': None, 'period_start': '2024-01-30', 'period_end': '2024-01-01'}
        form = LaptopForm(data=laptop_data)
        self.assertFalse(form.is_valid())
