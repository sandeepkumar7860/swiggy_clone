from django.contrib import admin
from .models import Restaurant, MenuItem, Address, Cart, CartItem, Order, OrderItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name','address','is_active')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name','restaurant','price','available')

admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
