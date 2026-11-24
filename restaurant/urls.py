
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # FOOD MANAGEMENT
    path('foods/', views.food_list, name='food_list'),
    path('foods/add/', views.food_add, name='food_add'),
    path('foods/edit/<int:pk>/', views.food_update, name='food_update'),
    path('foods/delete/<int:pk>/', views.food_delete, name='food_delete'),

    # CATEGORY MANAGEMENT
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    # CUSTOMER MANAGEMENT
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_add, name='customer_add'),
    path('customers/edit/<int:pk>/', views.customer_edit, name='customer_edit'),
    path('customers/delete/<int:pk>/', views.customer_delete, name='customer_delete'),

    # ORDER MANAGEMENT
    path('orders/', views.order_list, name='order_list'),
    path('orders/update-status/<int:pk>/', views.order_update_status, name='order_update_status'),
]
