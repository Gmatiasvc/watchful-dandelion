from django.test import TestCase, Client
from django.urls import reverse

class AppViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_registro_view_status_code(self):
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)

    def test_lector_view_status_code(self):
        response = self.client.get(reverse('lector'))
        self.assertEqual(response.status_code, 200)
