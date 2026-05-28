# LUXECART — Full-Stack E-Commerce Store
> Premium e-commerce site with Django backend & vanilla JS frontend. All prices in **INR (₹)**

---

## 📁 Project Structure

```
ecommerce/                   ← Frontend (open index.html in browser)
├── index.html               ← Main storefront
├── static/
│   ├── css/
│   │   ├── style.css        ← Global styles, components, modals
│   │   └── home.css         ← Hero, categories, product grid
│   └── js/
│       ├── data.js          ← 12 product catalogue (INR prices)
│       ├── auth.js          ← Login/Register (localStorage)
│       ├── cart.js          ← Cart sidebar, qty, totals
│       └── app.js           ← Products, modal, checkout, toast

luxecart_backend/            ← Django REST backend
├── manage.py
├── db.sqlite3               ← SQLite database
├── luxecart_backend/
│   ├── settings.py
│   └── urls.py
└── store/
    ├── models.py            ← User, Product, Category, Order, Cart, Review
    ├── views.py             ← All API views
    ├── urls.py              ← API routes
    ├── admin.py             ← Django admin config
    └── management/commands/
        └── seed_data.py     ← Seed products & categories
```

---

## 🌟 Features

### Frontend
| Feature | Details |
|---|---|
| 🛍️ Product Grid | 12 curated products with filtering by category |
| 🔍 Quick View Modal | Full product detail with qty selector, features, savings |
| 🛒 Shopping Cart Sidebar | Slide-in cart with subtotal, GST (18%), delivery, grand total |
| ❤️ Wishlist | Toggle wishlist on any product |
| 👤 Auth Modal | Register / Login with localStorage persistence |
| 📦 Checkout | 2-step checkout — address → payment method |
| ✅ Order Confirmation | Order ID generated, saved to localStorage |
| 🔔 Toast Notifications | Non-intrusive feedback for all actions |
| 📱 Responsive Design | Mobile-first across all screen sizes |

### Backend (Django REST API)
| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/auth/register/` | POST | Create account |
| `/api/v1/auth/login/` | POST | Sign in |
| `/api/v1/auth/logout/` | POST | Sign out |
| `/api/v1/auth/me/` | GET | Current user |
| `/api/v1/products/` | GET | List products (filter: `?category=`, `?q=`) |
| `/api/v1/products/:id/` | GET | Product detail |
| `/api/v1/categories/` | GET | All categories |
| `/api/v1/cart/` | GET | View cart |
| `/api/v1/cart/add/` | POST | Add to cart |
| `/api/v1/cart/remove/:id/` | DELETE | Remove item |
| `/api/v1/orders/place/` | POST | Place order |
| `/api/v1/orders/` | GET | Order history |
| `/api/v1/orders/:id/` | GET | Order detail |

---

## 🚀 Setup & Run

### Frontend (Zero Setup)
```bash
# Simply open in browser:
open ecommerce/index.html
# OR serve with Python:
cd ecommerce && python -m http.server 8080
# Then visit: http://localhost:8080
```

### Backend (Django)
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install django djangorestframework django-cors-headers

# 3. Navigate to backend
cd luxecart_backend

# 4. Run migrations
python manage.py migrate

# 5. Seed product data
python manage.py seed_data

# 6. Create superuser (admin)
python manage.py createsuperuser

# 7. Start server
python manage.py runserver

# API available at: http://localhost:8000/api/v1/
# Admin panel:       http://localhost:8000/admin/
```

---

## 💰 Pricing & Tax Logic
- All prices displayed in **Indian Rupees (₹)**
- **GST**: 18% applied on subtotal
- **Delivery**: ₹99 flat | **FREE** for orders above ₹999
- Discounts shown as percentage + savings amount

## 🗄️ Database Models
- **User** — Extended AbstractUser with phone, address, city, state, pincode
- **Category** — Product categories with slug & icon
- **Product** — Full product with INR pricing, stock, rating, features (JSONField), badge
- **Order** — Complete order with address snapshot, financials, status tracking
- **OrderItem** — Snapshot of product at purchase time
- **CartItem** — Server-side persistent cart
- **Review** — Product reviews with verified purchase flag

## 🔒 Security Notes (Production Checklist)
- [ ] Change `SECRET_KEY` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Add `django-cors-headers` and configure CORS properly
- [ ] Serve media/static files via Nginx/S3
- [ ] Enable HTTPS/SSL

---
*Built for CodeAlpha Internship Task — E-Commerce Store*
