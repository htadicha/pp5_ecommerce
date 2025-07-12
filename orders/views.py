import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
import datetime
import json
from django.http import JsonResponse
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Set the Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

def place_order(request, total=0, quantity=0):
    """
    Handles the submission of the checkout form and saves the order.
    """
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            
            # Pass order details and Stripe public key to the payments view
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')

def payments(request):
    """
    Creates a Stripe Checkout session and redirects the user.
    """
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Create Stripe Checkout Session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Hawashmart Order ' + order.order_number,
                    },
                    'unit_amount': int(order.order_total * 100), # Amount in cents
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(f"/orders/order_complete/?order_number={order.order_number}&payment_id={{CHECKOUT_SESSION_ID}}"),
        cancel_url=request.build_absolute_uri('/store/'),
    )
    
    return JsonResponse({'sessionId': checkout_session.id})

def order_complete(request):
    """
    Handles the successful payment return from Stripe.
    """
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        # Find the order that is not yet marked as ordered
        order = Order.objects.get(order_number=order_number, is_ordered=False)

        # Create the payment record now that payment is successful
        payment = Payment(
            user = request.user,
            payment_id = transID,
            payment_method = 'Stripe',
            amount_paid = order.order_total,
            status = 'Completed', # Mark as completed immediately
        )
        payment.save()

        # Update the order with payment and set as ordered
        order.payment = payment
        order.is_ordered = True
        order.save()

        # Move cart items to Order Product table
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # Clear cart
        CartItem.objects.filter(user=request.user).delete()

        # TODO: Send order recieved email to customer

        # Prepare context for the template
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
