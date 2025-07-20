from django.test import TestCase
from django.urls import reverse


class HealthCheckTestCase(TestCase):
    def test_health_check_returns_200(self):
        response = self.client.get(reverse("accounts:health-check"))
        self.assertEqual(response.status_code, 200)

    def test_health_check_returns_correct_data(self):
        response = self.client.get(reverse("accounts:health-check"))
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "core")
        self.assertEqual(data["version"], "0.1.0")
