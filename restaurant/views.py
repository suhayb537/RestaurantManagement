
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count

from .models import Category, Food, Customer, Order
from .forms import FoodForm, CategoryForm, CustomerForm, OrderStatusForm


# =====================================
# DASHBOARD
# =====================================

def dashboard(request):
    context = {
        'total_categories': Category.objects.count(),
        'total_foods': Food.objects.count(),
        'total_customers': Customer.objects.count(),
        'total_orders': Order.objects.count(),

        'available_foods': Food.objects.filter(available=True).count(),
        'unavailable_foods': Food.objects.filter(available=False).count(),

        'pending_orders': Order.objects.filter(status='Pending').count(),

        'latest_orders': Order.objects.select_related(
            'customer'
        ).order_by('-id')[:5],
    }

    return render(request, 'restaurant/dashboard.html', context)


# =====================================
# FOOD MANAGEMENT
# =====================================

def food_list(request):
    search = request.GET.get('search', '').strip()

    foods = Food.objects.select_related(
        'category'
    ).all().order_by('-id')

    if search:
        foods = foods.filter(
            Q(name__icontains=search) |
            Q(category__name__icontains=search) |
            Q(description__icontains=search)
        )

    context = {
        'foods': foods,
        'search': search,
        'available_count': Food.objects.filter(available=True).count(),
        'unavailable_count': Food.objects.filter(available=False).count(),
    }

    return render(request, 'restaurant/food_list.html', context)


def food_add(request):
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Food added successfully!')
            return redirect('food_list')
    else:
        form = FoodForm()

    return render(request, 'restaurant/food_form.html', {
        'form': form,
        'title': 'Add New Food'
    })


def food_update(request, pk):
    food = get_object_or_404(Food, pk=pk)

    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES, instance=food)

        if form.is_valid():
            form.save()
            messages.success(request, 'Food updated successfully!')
            return redirect('food_list')
    else:
        form = FoodForm(instance=food)

    return render(request, 'restaurant/food_form.html', {
        'form': form,
        'title': 'Update Food'
    })


def food_delete(request, pk):
    food = get_object_or_404(Food, pk=pk)

    if request.method == 'POST':
        food.delete()
        messages.success(request, 'Food deleted successfully!')
        return redirect('food_list')

    return render(request, 'restaurant/food_confirm_delete.html', {
        'food': food
    })


# =====================================
# CATEGORY MANAGEMENT
# =====================================

def category_list(request):
    search = request.GET.get('search', '').strip()

    categories = Category.objects.annotate(
        food_count=Count('foods')
    ).order_by('-id')

    if search:
        categories = categories.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    context = {
        'categories': categories,
        'search': search,
        'total_categories': Category.objects.count(),
    }

    return render(request, 'restaurant/category_list.html', context)


def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'restaurant/category_form.html', {
        'form': form,
        'page_title': 'Add New Category'
    })


def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'restaurant/category_form.html', {
        'form': form,
        'page_title': 'Edit Category'
    })


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')

    return render(request, 'restaurant/category_confirm_delete.html', {
        'category': category
    })


# =====================================
# CUSTOMER MANAGEMENT
# =====================================

def customer_list(request):
    search = request.GET.get('search', '').strip()

    customers = Customer.objects.all().order_by('-id')

    if search:
        customers = customers.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search) |
            Q(address__icontains=search)
        )

    context = {
        'customers': customers,
        'search': search,
        'total_customers': Customer.objects.count(),
    }

    return render(request, 'restaurant/customer_list.html', context)


def customer_add(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'restaurant/customer_form.html', {
        'form': form,
        'page_title': 'Add New Customer'
    })


def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'restaurant/customer_form.html', {
        'form': form,
        'page_title': 'Edit Customer'
    })


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return redirect('customer_list')

    return render(request, 'restaurant/customer_confirm_delete.html', {
        'customer': customer
    })


# =====================================
# ORDER MANAGEMENT
# =====================================

def order_list(request):
    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    orders = Order.objects.select_related(
        'customer'
    ).prefetch_related(
        'items__food'
    ).order_by('-id')

    if search:
        orders = orders.filter(
            Q(customer__name__icontains=search) |
            Q(customer__phone__icontains=search) |
            Q(id__icontains=search)
        )

    if status:
        orders = orders.filter(status=status)

    context = {
        'orders': orders,
        'search': search,
        'selected_status': status,

        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='Pending').count(),
        'preparing_orders': Order.objects.filter(status='Preparing').count(),
        'ready_orders': Order.objects.filter(status='Ready').count(),
        'delivered_orders': Order.objects.filter(status='Delivered').count(),
    }

    return render(request, 'restaurant/order_list.html', context)


def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            messages.success(request, 'Order status updated successfully!')
        else:
            messages.error(request, 'Please select a valid order status.')

    return redirect('order_list')
