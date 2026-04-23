from rest_framework import serializers
from .models import Restaurant, MenuItem, Order, OrderItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)
    class Meta:
        model = Restaurant
        fields = '__all__'
