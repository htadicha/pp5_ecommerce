from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.shortcuts import render, get_object_or_404, redirect

from accounts.decorators import admin_required
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from orders.models import OrderProduct
from .forms import ProductForm, ReviewForm
from .models import Product, ProductGallery, ReviewRating


def store(request, category_slug=None):
    """
    Display products with optional category filtering, sorting, and pagination.
    """
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)

    sort_option = request.GET.get("sort")

    if sort_option == "price_lh":
        products = products.order_by("price")
    elif sort_option == "alpha_az":
        products = products.order_by("product_name")
    elif sort_option == "alpha_za":
        products = products.order_by("-product_name")
    elif sort_option == "rating":
        products = products.annotate(avg_rating=Avg("reviewrating__rating")).order_by(
            "-avg_rating"
        )
    else:
        products = products.order_by("-created_date")

    paginator = Paginator(products, 16)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        "products": paged_products,
        "product_count": product_count,
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    """
    Display detailed product information with reviews and gallery.
    """
    try:
        # Get the single product
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
        # Check if the product is already in the cart
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product
        ).exists()
    except Exception as e:
        # It's better to handle specific exceptions, but for now we'll re-raise
        raise e

    # Check if the user has purchased this product before to allow reviews
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(
                user=request.user, product_id=single_product.id
            ).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews and gallery images for the product
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    # The context now only needs the single_product. The template will handle
    # accessing the variations via `single_product.variation_set.all()`
    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "orderproduct": orderproduct,
        "reviews": reviews,
        "product_gallery": product_gallery,
    }
    return render(request, "store/product_detail.html", context)


def search(request):
    """
    Search products by name or description keywords.
    """
    products = None  # Initialize products to None
    product_count = 0
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            product_count = products.count()
    context = {
        "products": products,
        "product_count": product_count,
    }
    return render(request, "store/store.html", context)


@login_required(login_url="login")
def submit_review(request, product_id):
    """
    Submit or update a product review.
    """
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id
            )
            form = ReviewForm(request.POST, instance=reviews)
            if form.is_valid():
                form.save()
                messages.success(request, "Thank you! Your review has been updated.")
                return redirect(url)
            messages.error(request, "Please correct the errors below.")
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)
            messages.error(request, "Please correct the errors below.")
    return redirect(url)


@login_required(login_url="login")
@admin_required
def manage_products(request):
    """
    Display a paginated list of products for admins to manage.
    """

    products = Product.objects.order_by("-modified_date")
    context = {
        "products": products,
    }
    return render(request, "store/manage/product_list.html", context)


@login_required(login_url="login")
@admin_required
def create_product(request):
    """
    Allow admins to create a new product through the front-end dashboard.
    """

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully.")
            return redirect("manage_products")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm()
    return render(
        request,
        "store/manage/product_form.html",
        {
            "form": form,
            "title": "Add Product",
            "submit_label": "Create Product",
        },
    )


@login_required(login_url="login")
@admin_required
def update_product(request, slug):
    """
    Allow admins to edit existing product details.
    """

    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("manage_products")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        "store/manage/product_form.html",
        {
            "form": form,
            "title": f"Edit {product.product_name}",
            "submit_label": "Save Changes",
        },
    )


@login_required(login_url="login")
@admin_required
def delete_product(request, slug):
    """
    Allow admins to confirm and delete a product entry.
    """

    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect("manage_products")
    return render(
        request,
        "store/manage/product_confirm_delete.html",
        {
            "product": product,
        },
    )


@login_required(login_url="login")
def edit_review(request, review_id):
    """
    Permit reviewers to edit their previous review submissions.
    """

    review = get_object_or_404(ReviewRating, pk=review_id, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated.")
            return redirect(review.product.get_url())
        messages.error(request, "Please correct the errors below.")
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "store/review_form.html",
        {
            "form": form,
            "product": review.product,
        },
    )


@login_required(login_url="login")
def delete_review(request, review_id):
    """
    Provide a confirmation flow for reviewers to delete their feedback.
    """

    review = get_object_or_404(ReviewRating, pk=review_id, user=request.user)
    product_url = review.product.get_url()
    if request.method == "POST":
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect(product_url)
    return render(
        request,
        "store/review_confirm_delete.html",
        {
            "review": review,
        },
    )
