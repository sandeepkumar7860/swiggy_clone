from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_veg = models.BooleanField(default=False)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} — {self.restaurant.name}"

class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    label = models.CharField(max_length=50, default='Home')
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.label} — {self.user}"

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.menu_item.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('PLACED','Placed'),
        ('CONFIRMED','Confirmed'),
        ('PREPARING','Preparing'),
        ('OUT_FOR_DELIVERY','Out for delivery'),
        ('DELIVERED','Delivered'),
        ('CANCELED','Canceled'),
    ]
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)
    placed_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLACED')
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # snapshot price

