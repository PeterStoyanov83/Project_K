from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory
from clients.admin import ClientAdmin
from clients.models import Client
from datetime import date


class ClientModelTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            name="Test Client",
            location="office_center",
            date_of_entry=date.today(),
            signed_agreement=True,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.client), "Test Client")

    def test_location_label(self):
        field_label = self.client._meta.get_field('location').verbose_name
        self.assertEqual(field_label, 'location')


def has_perm():
    return True


class MockSuperUser:
    pass


request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = has_perm()


class ClientAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_admin_list_display(self):
        client_admin = ClientAdmin(Client, self.site)
        self.assertEqual(
            list(client_admin.get_list_display(request)),
            ['name', 'location', 'date_of_entry', 'date_of_exit', 'signed_agreement']
        )
