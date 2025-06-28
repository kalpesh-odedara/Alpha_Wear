
# 2. ecommerce/settings.py
INSTALLED_APPS = [
    ...,
    'store',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 3. ecommerce/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 4. store/models.py
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)

# 5. store/admin.py
from django.contrib import admin
from .models import Product, Order

admin.site.register(Product)
admin.site.register(Order)

# 6. store/views.py
from django.shortcuts import render, redirect
from .models import Product, Order
from django.contrib.auth.decorators import login_required

# Show all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# Add product to cart
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    Order.objects.create(user=request.user, product=product)
    return redirect('cart')

# View cart
@login_required
def cart(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/cart.html', {'orders': orders})

# 7. store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='home'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]

# 8. Templates Folder Structure
# Create: store/templates/store/product_list.html
# Example HTML:
# <!DOCTYPE html>
# <html><body>
#   <h1>Product List</h1>
#   {% for product in products %}
#     <div>
#       <h3>{{ product.name }}</h3>
#       <p>{{ product.description }}</p>
#       <p>Price: ₹{{ product.price }}</p>
#       <a href="{% url 'add_to_cart' product.id %}">Add to Cart</a>
#     </div>
#   {% endfor %}
# </body></html>

# Create: store/templates/store/cart.html
# <!DOCTYPE html>
# <html><body>
#   <h1>Your Cart</h1>
#   {% for order in orders %}
#     <p>{{ order.product.name }} - Quantity: {{ order.quantity }}</p>
#   {% empty %}
#     <p>No items in cart.</p>
#   {% endfor %}
# </body></html>

# 9. Run these commands:
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser
# python manage.py runserver