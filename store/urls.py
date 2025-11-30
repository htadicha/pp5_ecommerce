from django.urls import path
from . import views

urlpatterns = [
    # The empty path for the main store page
    path("", views.store, name="store"),
    # The more specific URL for product details must come BEFORE the general category URL
    path(
        "category/<slug:category_slug>/<slug:product_slug>/",
        views.product_detail,
        name="product_detail",
    ),
    # The general category URL
    path("category/<slug:category_slug>/", views.store, name="products_by_category"),
    # Other URLs
    path("search/", views.search, name="search"),
    path("submit_review/<int:product_id>/", views.submit_review, name="submit_review"),
    path("reviews/<int:review_id>/edit/", views.edit_review, name="edit_review"),
    path("reviews/<int:review_id>/delete/", views.delete_review, name="delete_review"),
    path("manage/products/", views.manage_products, name="manage_products"),
    path("manage/products/add/", views.create_product, name="create_product"),
    path(
        "manage/products/<slug:slug>/edit/",
        views.update_product,
        name="update_product",
    ),
    path(
        "manage/products/<slug:slug>/delete/",
        views.delete_product,
        name="delete_product",
    ),
]
