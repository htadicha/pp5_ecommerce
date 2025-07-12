from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1 # Allows adding one extra variation form by default
    list_display = ('variation_category', 'variation_value', 'is_active')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [VariationInline, ProductGalleryInline] # Add VariationInline here

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
