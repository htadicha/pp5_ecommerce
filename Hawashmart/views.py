from django.shortcuts import render
from store.models import Product, ReviewRating
from django.db.models import Q

def home(request):
    # Fetch products that are available AND are either new OR trending.
    # Order by the most recently created date first.
    products = Product.objects.filter(
        Q(is_new=True) | Q(is_trending=True),
        is_available=True
    ).order_by('-created_date')

    context = {
        'products': products,
    }
    return render(request, 'home.html', context)