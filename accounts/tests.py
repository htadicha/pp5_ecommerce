"""
Tests covering the critical registration and activation flows.
"""

from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.models import Account


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="noreply@testserver.com",
)
class RegistrationFlowTests(TestCase):
    """Ensure users can register and activate their accounts successfully."""

    def _registration_payload(self, email="customer@example.com"):
        return {
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+123456789",
            "email": email,
            "password": "ComplexPass123",
            "confirm_password": "ComplexPass123",
        }

    def test_register_creates_inactive_user_and_sends_email(self):
        """Registration should persist a user and send a verification email."""
        payload = self._registration_payload()
        response = self.client.post(reverse("register"), data=payload)

        self.assertEqual(response.status_code, 302)
        expected_redirect = "/accounts/login/?command=verification&email=customer@example.com"
        self.assertEqual(response.url, expected_redirect)

        user = Account.objects.get(email=payload["email"])
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("activate your account", mail.outbox[0].subject.lower())
        self.assertIn(payload["email"], mail.outbox[0].to)

    def test_activation_endpoint_marks_user_as_active(self):
        """Activation endpoint should flip the user to active when token valid."""
        user = Account.objects.create_user(
            first_name="Inactive",
            last_name="User",
            username="inactive-user",
            email="inactive@example.com",
            password="Testpass123",
        )
        self.assertFalse(user.is_active)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        response = self.client.get(reverse("activate", args=[uid, token]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))

        user.refresh_from_db()
        self.assertTrue(user.is_active)
