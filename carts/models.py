from django.db import models
from store.models import Product, Variation
from accounts.models import Account


class Cart(models.Model):
    """
    Model for shopping cart sessions.
    
    Represents a shopping cart session that can contain multiple cart items.
    Each cart is identified by a unique cart_id and tracks when it was created.
    Used for both guest and authenticated user shopping sessions.
    """
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        """Return the cart ID as string representation."""
        return self.cart_id


class CartItem(models.Model):
    """
    Model for individual items in shopping cart.
    
    Represents a single product item added to a shopping cart. Can include
    product variations (color, size) and quantity. Links to both user account
    (for authenticated users) and cart session (for guest users).
    """
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        """Calculate the subtotal for this cart item."""
        return self.product.price * self.quantity

    def __unicode__(self):
        """Return the product as string representation."""
        return self.product
