from django.test import TestCase
from django.urls import reverse

from marketing.models import NewsletterSignup


class NewsletterSignupViewTests(TestCase):
    """Ensure newsletter subscriptions create or reuse records."""

    def test_subscribe_creates_record(self):
        response = self.client.post(reverse("marketing:newsletter_subscribe"), {"email": "new@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(NewsletterSignup.objects.filter(email="new@example.com").exists())

    def test_duplicate_subscription_shows_info(self):
        NewsletterSignup.objects.create(email="existing@example.com")
        response = self.client.post(reverse("marketing:newsletter_subscribe"), {"email": "existing@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(NewsletterSignup.objects.filter(email="existing@example.com").count(), 1)
