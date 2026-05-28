from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
import json

from .models import User, Category, Product, Order, OrderItem, CartItem, Review


# ─── HELPERS ────────────────────────────────────────────────────────────────
def json_response(data, status=200):
    return JsonResponse(data, status=status, json_dumps_params={'ensure_ascii': False})

def error(msg, status=400):
    return json_response({'success': False, 'error': msg}, status)

def success(data=None, msg='OK'):
    return json_response({'success': True, 'message': msg, **(data or {})})

def product_to_dict(p):
    return {
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'category': p.category.slug if p.category else None,
        'price': float(p.price),
        'original_price': float(p.original_price) if p.original_price else None,
        'discount_percent': p.discount_percent,
        'image_url': p.image_url,
        'stock': p.stock,
        'rating': float(p.rating),
        'review_count': p.review_count,
        'badge': p.badge,
        'features': p.features,
        'is_active': p.is_active,
    }

def order_to_dict(o):
    return {
        'order_id': o.order_id,
        'status': o.status,
        'payment_method': o.payment_method,
        'subtotal': float(o.subtotal),
        'gst_amount': float(o.gst_amount),
        'delivery_charge': float(o.delivery_charge),
        'grand_total': float(o.grand_total),
        'created_at': o.created_at.isoformat(),
        'shipping': {
            'name': o.shipping_name,
            'phone': o.shipping_phone,
            'address': o.shipping_address,
            'city': o.shipping_city,
            'state': o.shipping_state,
            'pincode': o.shipping_pincode,
        },
        'items': [
            {
                'name': i.product_name,
                'image': i.product_image,
                'qty': i.quantity,
                'unit_price': float(i.unit_price),
                'total': float(i.total_price),
            } for i in o.items.all()
        ],
    }


# ─── AUTH VIEWS ─────────────────────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return error("Invalid JSON")

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()

    if not email or not password or not first_name:
        return error("Name, email and password are required")
    if len(password) < 6:
        return error("Password must be at least 6 characters")
    if User.objects.filter(email=email).exists():
        return error("Email already registered")

    user = User.objects.create_user(
        username=email, email=email, password=password,
        first_name=first_name, last_name=last_name,
        phone=data.get('phone', ''),
    )
    login(request, user)
    return success({
        'user': {'id': user.id, 'name': user.get_full_name(), 'email': user.email}
    }, "Registration successful")


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return error("Invalid JSON")

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    user = authenticate(request, username=email, password=password)
    if not user:
        return error("Invalid email or password", 401)

    login(request, user)
    return success({
        'user': {'id': user.id, 'name': user.get_full_name(), 'email': user.email}
    }, "Login successful")


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return success(msg="Logged out")


@require_http_methods(["GET"])
def me_view(request):
    if not request.user.is_authenticated:
        return error("Not authenticated", 401)
    u = request.user
    return success({'user': {'id': u.id, 'name': u.get_full_name(), 'email': u.email, 'phone': u.phone}})


# ─── PRODUCT VIEWS ───────────────────────────────────────────────────────────
@require_http_methods(["GET"])
def product_list(request):
    qs = Product.objects.filter(is_active=True).select_related('category')
    cat_slug = request.GET.get('category')
    if cat_slug:
        qs = qs.filter(category__slug=cat_slug)
    search = request.GET.get('q')
    if search:
        qs = qs.filter(name__icontains=search)

    products = [product_to_dict(p) for p in qs]
    return json_response({'products': products, 'count': len(products)})


@require_http_methods(["GET"])
def product_detail(request, pk):
    p = get_object_or_404(Product, pk=pk, is_active=True)
    return json_response(product_to_dict(p))


# ─── CART VIEWS ──────────────────────────────────────────────────────────────
@login_required
@require_http_methods(["GET"])
def cart_view(request):
    items = CartItem.objects.filter(user=request.user).select_related('product')
    return json_response({
        'items': [
            {'product': product_to_dict(i.product), 'quantity': i.quantity}
            for i in items
        ]
    })


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def cart_add(request):
    data = json.loads(request.body)
    product = get_object_or_404(Product, pk=data.get('product_id'))
    qty = int(data.get('quantity', 1))

    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    item.quantity = min(item.quantity + qty if not created else qty, product.stock)
    item.save()
    return success(msg="Added to cart")


@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def cart_remove(request, product_id):
    CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    return success(msg="Removed from cart")


# ─── ORDER VIEWS ──────────────────────────────────────────────────────────────
@csrf_exempt
@login_required
@require_http_methods(["POST"])
def place_order(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return error("Invalid JSON")

    items_data = data.get('items', [])
    if not items_data:
        return error("Cart is empty")

    subtotal = 0
    order_items = []

    with transaction.atomic():
        # Validate products & stock
        for item in items_data:
            product = get_object_or_404(Product, pk=item['product_id'])
            qty = int(item['quantity'])
            if product.stock < qty:
                return error(f"Insufficient stock for {product.name}")
            subtotal += float(product.price) * qty
            order_items.append((product, qty))

        gst = round(subtotal * 0.18, 2)
        delivery = 0 if subtotal > 999 else 99
        grand_total = subtotal + gst + delivery

        order = Order.objects.create(
            user=request.user,
            payment_method=data.get('payment_method', 'cod'),
            shipping_name=data.get('shipping_name', ''),
            shipping_phone=data.get('shipping_phone', ''),
            shipping_address=data.get('shipping_address', ''),
            shipping_city=data.get('shipping_city', ''),
            shipping_state=data.get('shipping_state', ''),
            shipping_pincode=data.get('shipping_pincode', ''),
            subtotal=subtotal,
            gst_amount=gst,
            delivery_charge=delivery,
            grand_total=grand_total,
        )

        for product, qty in order_items:
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                product_image=product.image_url,
                quantity=qty,
                unit_price=product.price,
            )
            # Deduct stock
            product.stock -= qty
            product.save(update_fields=['stock'])

        # Clear server-side cart
        CartItem.objects.filter(user=request.user).delete()

    return success({'order': order_to_dict(order)}, "Order placed successfully")


@login_required
@require_http_methods(["GET"])
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return json_response({'orders': [order_to_dict(o) for o in orders]})


@login_required
@require_http_methods(["GET"])
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return json_response(order_to_dict(order))


# ─── CATEGORIES ──────────────────────────────────────────────────────────────
@require_http_methods(["GET"])
def category_list(request):
    cats = Category.objects.all()
    return json_response({
        'categories': [
            {'id': c.id, 'name': c.name, 'slug': c.slug, 'icon': c.icon}
            for c in cats
        ]
    })
