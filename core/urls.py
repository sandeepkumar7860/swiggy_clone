from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('login/', views.login_register_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('cart/', views.view_cart, name='cart'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    
]
