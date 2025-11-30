"""
Tests covering store review CRUD and admin product management flows.
"""

import shutil

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import Account
from category.models import Category
from store.models import Product, ReviewRating


def _generate_image_file():
    """Return a lightweight in-memory image for test uploads."""

    return SimpleUploadedFile(
        "test.gif",
        b"GIF87a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!"
        b"\xf9\x04\x01\n\x00\x01\x00,\x00\x00\x00\x00\x01\x00\x01\x00"
        b"\x00\x02\x02D\x01\x00;",
        content_type="image/gif",
    )


TEST_MEDIA_ROOT = settings.BASE_DIR / "test-media"


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ReviewCrudTests(TestCase):
    """Ensure customers can edit and delete their own reviews."""

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(category_name="Shoes", slug="shoes")
        cls.product = Product.objects.create(
            product_name="Runner",
            slug="runner",
            description="Lightweight shoes",
            price=50,
            stock=10,
            category=cls.category,
            images=_generate_image_file(),
        )
        cls.customer = Account.objects.create_user(
            first_name="Jane",
            last_name="Doe",
            username="janedoe",
            email="jane@example.com",
            password="Testpass123",
        )
        cls.customer.is_active = True
        cls.customer.save()
        cls.review = ReviewRating.objects.create(
            product=cls.product,
            user=cls.customer,
            subject="Great",
            review="Comfortable and light",
            rating=4,
            ip="127.0.0.1",
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.client.login(email="jane@example.com", password="Testpass123")

    def test_edit_review_updates_content(self):
        """Posting to edit_review should persist the new values."""

        response = self.client.post(
            reverse("edit_review", args=[self.review.id]),
            data={"subject": "Updated", "review": "Even better after a month", "rating": 4.5},
        )
        self.assertRedirects(response, self.product.get_url())
        refreshed = ReviewRating.objects.get(pk=self.review.id)
        self.assertEqual(refreshed.subject, "Updated")
        self.assertAlmostEqual(refreshed.rating, 4.5)

    def test_delete_review_removes_record(self):
        """Deleting a review should remove it from the database."""

        response = self.client.post(reverse("delete_review", args=[self.review.id]))
        self.assertRedirects(response, self.product.get_url())
        self.assertFalse(ReviewRating.objects.filter(pk=self.review.id).exists())


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProductManagementTests(TestCase):
    """Validate that only admins can access the product management dashboard."""

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(category_name="Bags", slug="bags")
        cls.product = Product.objects.create(
            product_name="Day Pack",
            slug="day-pack",
            description="Durable day pack",
            price=80,
            stock=5,
            category=cls.category,
            images=_generate_image_file(),
        )
        cls.user = Account.objects.create_user(
            first_name="John",
            last_name="Smith",
            username="johnsmith",
            email="john@example.com",
            password="Testpass123",
        )
        cls.user.is_active = True
        cls.user.save()
        cls.admin = Account.objects.create_user(
            first_name="Admin",
            last_name="User",
            username="adminuser",
            email="admin@example.com",
            password="Adminpass123",
        )
        cls.admin.is_staff = True
        cls.admin.is_admin = True
        cls.admin.is_active = True
        cls.admin.save()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def test_manage_products_redirects_non_admin(self):
        """Regular customers should be redirected away from the admin dashboard."""

        self.client.login(email="john@example.com", password="Testpass123")
        response = self.client.get(reverse("manage_products"))
        self.assertRedirects(response, reverse("dashboard"))

    def test_manage_products_available_for_admin(self):
        """Staff members can load the product management table."""

        self.client.login(email="admin@example.com", password="Adminpass123")
        response = self.client.get(reverse("manage_products"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Day Pack")
