from django.test import TestCase
from django.urls import reverse
from .models import Client
from .forms import ClientForm


class ClientModelTests(TestCase):

    def test_create_client(self):
        # Test creating a Client instance
        client = Client.objects.create(name="Test Client", location="office_center")
        self.assertEqual(client.name, "Test Client")

class ClientViewTests(TestCase):
    def test_client_profile_view(self):
        # Create a sample client
        client = Client.objects.create(name="Test Client", location="office_center")

        # Test the client_profile_view
        response = self.client.get(reverse('clients:client_profile_view', args=[client.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Client")
