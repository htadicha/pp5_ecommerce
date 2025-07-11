from django.urls import path
from . import views

urlpatterns = [
    # Change the name from 'store' to 'home' to match the template
    path('', views.store, name='home'),
    
    # This path allows you to still refer to the store page with the name 'store' if needed elsewhere
    path('store/', views.store, name='store'), 

    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]