from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/',    views.login_view,    name='login'),
    path('auth/logout/',   views.logout_view,   name='logout'),
    path('auth/me/',       views.me_view,        name='me'),

    # Products
    path('products/',          views.product_list,   name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),

    # Categories
    path('categories/', views.category_list, name='category-list'),

    # Cart
    path('cart/',                         views.cart_view,   name='cart'),
    path('cart/add/',                     views.cart_add,    name='cart-add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart-remove'),

    # Orders
    path('orders/',              views.order_list,   name='order-list'),
    path('orders/place/',        views.place_order,  name='place-order'),
    path('orders/<str:order_id>/', views.order_detail, name='order-detail'),
]
