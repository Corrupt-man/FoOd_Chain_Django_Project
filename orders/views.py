from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm, CheckoutForm
from .models import FoodItem, Order, OrderItem

DELIVERY_FEE = Decimal("150.00")

def register(request):
    if request.user.is_authenticated:
        return redirect("menu")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to FoOd Chain®!")
        return redirect("menu")
    return render(request, "orders/register.html", {"form": form})

def menu(request):
    foods = FoodItem.objects.filter(available=True)
    category = request.GET.get("category", "")
    if category:
        foods = foods.filter(category=category)
    categories = FoodItem.CATEGORY_CHOICES
    return render(request, "orders/menu.html", {"foods": foods, "categories": categories, "selected_category": category})

def _cart_details(request):
    cart = request.session.get("cart", {})
    items, subtotal = [], Decimal("0.00")
    for food_id, quantity in cart.items():
        try:
            food = FoodItem.objects.get(pk=int(food_id), available=True)
            quantity = max(1, min(int(quantity), 99))
        except (FoodItem.DoesNotExist, ValueError, TypeError):
            continue
        line_total = food.price * quantity
        subtotal += line_total
        items.append({"food": food, "quantity": quantity, "line_total": line_total})
    return items, subtotal

def cart_view(request):
    items, subtotal = _cart_details(request)
    return render(request, "orders/cart.html", {
        "items": items, "subtotal": subtotal,
        "delivery_fee": DELIVERY_FEE if items else Decimal("0.00"),
        "total": subtotal + (DELIVERY_FEE if items else Decimal("0.00")),
    })

def add_to_cart(request, food_id):
    if request.method != "POST":
        return redirect("menu")
    food = get_object_or_404(FoodItem, pk=food_id, available=True)
    cart = request.session.get("cart", {})
    key = str(food.pk)
    cart[key] = min(int(cart.get(key, 0)) + 1, 99)
    request.session["cart"] = cart
    messages.success(request, f"{food.name} added to your cart.")
    return redirect(request.POST.get("next") or "menu")

def update_cart(request, food_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        key = str(food_id)
        try:
            quantity = int(request.POST.get("quantity", "1"))
        except ValueError:
            quantity = 1
        if quantity <= 0:
            cart.pop(key, None)
        else:
            cart[key] = min(quantity, 99)
        request.session["cart"] = cart
    return redirect("cart")

def remove_from_cart(request, food_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        cart.pop(str(food_id), None)
        request.session["cart"] = cart
    return redirect("cart")

@login_required
def checkout(request):
    items, subtotal = _cart_details(request)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("menu")
    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        fee = DELIVERY_FEE
        total = subtotal + fee
        with transaction.atomic():
            order = Order.objects.create(
                customer=request.user,
                delivery_address=form.cleaned_data["delivery_address"],
                phone=form.cleaned_data["phone"],
                subtotal=subtotal, delivery_fee=fee, total=total,
            )
            for entry in items:
                food = entry["food"]
                OrderItem.objects.create(
                    order=order, food=food, food_name=food.name,
                    unit_price=food.price, quantity=entry["quantity"],
                    line_total=entry["line_total"],
                )
        request.session["cart"] = {}
        messages.success(request, "Order placed. Your bill is ready.")
        return redirect("bill", order_id=order.pk)
    return render(request, "orders/checkout.html", {
        "form": form, "items": items, "subtotal": subtotal,
        "delivery_fee": DELIVERY_FEE, "total": subtotal + DELIVERY_FEE,
    })

@login_required
def bill(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=order_id, customer=request.user)
    return render(request, "orders/bill.html", {"order": order})

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, "orders/history.html", {"orders": orders})
