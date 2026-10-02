from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
urlpatterns = [
    path("", views.menu, name="menu"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="orders/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:food_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:food_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:food_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("bill/<int:order_id>/", views.bill, name="bill"),
    path("orders/", views.order_history, name="order_history"),
]
