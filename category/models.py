from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Model for product categories.
    
    Represents product categories in the e-commerce system. Each category
    has a name, slug for URL generation, optional description, and image.
    Categories are used to organize products and enable filtering functionality.
    """
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        """Return the URL for the category products page."""
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        """Return the category name as string representation."""
        return self.category_name
