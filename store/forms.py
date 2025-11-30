from django import forms
from django.utils.text import slugify

from .models import Product, ReviewRating


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ["subject", "review", "rating"]


class ProductForm(forms.ModelForm):
    """Form used by admins to manage product catalog entries."""

    class Meta:
        model = Product
        fields = [
            "product_name",
            "slug",
            "category",
            "description",
            "price",
            "stock",
            "is_available",
            "is_trending",
            "is_new",
            "images",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        product_name = self.cleaned_data.get("product_name")
        if not slug and product_name:
            slug = slugify(product_name)
        return slug
