
from django import forms
from .models import Food, Category, Customer, Order


# =====================================
# FOOD FORM
# =====================================

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = [
            'category',
            'name',
            'description',
            'price',
            'available',
            'image'
        ]

        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter food name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Food description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
                'min': '0.01',
                'step': '0.01'
            }),
            'available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_price(self):
        price = self.cleaned_data['price']

        if price <= 0:
            raise forms.ValidationError(
                'Price must be greater than zero.'
            )

        return price


# =====================================
# CATEGORY FORM
# =====================================

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Category description'
            }),
        }


# =====================================
# CUSTOMER FORM
# =====================================

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name',
            'phone',
            'email',
            'address'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer full name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer address'
            }),
        }


# =====================================
# ORDER STATUS FORM
# =====================================

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
