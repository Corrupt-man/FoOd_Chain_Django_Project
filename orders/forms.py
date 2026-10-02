from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(
        label="Delivery address", widget=forms.Textarea(attrs={"rows": 3}),
        max_length=500
    )
    phone = forms.CharField(max_length=30, label="Phone number")
