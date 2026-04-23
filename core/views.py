from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Restaurant, MenuItem
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import get_user_model

User = get_user_model()

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'ok',
        'restaurants': Restaurant.objects.filter(is_active=True).count(),
        'message': 'Swiggy Clone is running!'
    })


def login_register_view(request):
    """Combined login and registration view"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Registration
        if action == 'register':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, f'Welcome {username}! Your account has been created.')
                return redirect('core:home')
            else:
                login_form = LoginForm()
                return render(request, 'core/login_register.html', {
                    'login_form': login_form,
                    'register_form': form,
                    'active_tab': 'register'
                })
        
        # Login
        elif action == 'login':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                
                user = authenticate(username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Welcome back {user.username}!')
                    return redirect('core:home')
                else:
                    messages.error(request, 'Invalid username or password.')
                
                register_form = RegistrationForm()
                return render(request, 'core/login_register.html', {
                    'login_form': form,
                    'register_form': register_form,
                    'active_tab': 'login'
                })
    
    else:
        login_form = LoginForm()
        register_form = RegistrationForm()
    
    return render(request, 'core/login_register.html', {
        'login_form': login_form,
        'register_form': register_form,
        'active_tab': 'login'
    })


def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('core:home')


class HomeListView(ListView):
    model = Restaurant
    template_name = 'core/home.html'
    context_object_name = 'restaurants'
    queryset = Restaurant.objects.filter(is_active=True)


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    items = restaurant.items.filter(available=True)
    return render(request, 'core/restaurant_detail.html', {'restaurant': restaurant, 'items': items})


# Correct helper function
@login_required(login_url='core:login')
def _get_or_create_cart(request):
    from .models import Cart
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


# ADD TO CART
@login_required(login_url='core:login')
def add_to_cart(request, item_id):
    from .models import CartItem
    menu_item = get_object_or_404(MenuItem, id=item_id)
    cart = _get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=menu_item
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('core:cart')


# VIEW CART
@login_required(login_url='core:login')
def view_cart(request):
    from .models import CartItem
    cart = _get_or_create_cart(request)
    items = cart.items.select_related('menu_item').all()
    subtotal = sum(ci.total_price for ci in items)
    context = {
        'cart': cart,
        'items': items,
        'subtotal': subtotal
    }
    return render(request, 'core/cart.html', context)


# UPDATE CART
@login_required(login_url='core:login')
def update_cart_item(request, item_id):
    from .models import CartItem
    action = request.POST.get('action')
    cart = _get_or_create_cart(request)
    ci = get_object_or_404(CartItem, cart=cart, id=item_id)
    if action == 'inc':
        ci.quantity += 1
        ci.save()
    elif action == 'dec':
        ci.quantity = max(1, ci.quantity - 1)
        ci.save()
    elif action == 'remove':
        ci.delete()
    return redirect('core:cart')


# CHECKOUT
@login_required(login_url='core:login')
def checkout(request):
    from .models import Order, OrderItem
    cart = _get_or_create_cart(request)
    items = cart.items.select_related('menu_item').all()
    if not items:
        return redirect('core:home')
    
    # Check if user has a default address
    address = request.user.addresses.filter(default=True).first()
    if not address:
        messages.error(request, 'Please add a delivery address first.')
        return redirect('core:login')
    
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=0,
            restaurant=items[0].menu_item.restaurant
        )
        total = 0
        for ci in items:
            OrderItem.objects.create(
                order=order,
                menu_item=ci.menu_item,
                quantity=ci.quantity,
                price=ci.menu_item.price,
            )
            total += ci.total_price
        order.total_amount = total
        order.save()
        cart.items.all().delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('core:order_history')
    else:
        subtotal = sum(ci.total_price for ci in items)
        return render(request, 'core/checkout.html', {'items': items, 'subtotal': subtotal, 'address': address})


# ORDER HISTORY
@login_required(login_url='core:login')
def order_history(request):
    orders = request.user.orders.order_by('-placed_at')
    return render(request, 'core/order_history.html', {'orders': orders})
