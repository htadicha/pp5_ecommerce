"""
Sitemaps for publicly accessible store pages.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product


class ProductSitemap(Sitemap):
    """Expose all available products for search engines."""

    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_available=True)

    def lastmod(self, obj):
        return obj.modified_date


class StaticViewSitemap(Sitemap):
    """List static marketing pages to include inside the sitemap."""

    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ["home", "store"]

    def location(self, item):
        return reverse(item)

