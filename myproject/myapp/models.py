from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone




# Create your models here.
class Register(AbstractUser):
    usertype=models.CharField(max_length=10,null=True)
    contact = models.CharField(max_length=10, null=True)
    
class Product(models.Model):
   
    name = models.CharField(max_length=255,null=True)
    category = models.CharField(max_length=100,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    image = models.ImageField(upload_to='product_images/',null=True)
    

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1,null=True)

ORDER_STATUS_CHOICES = [
    ('Placed', 'Placed'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
]

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1,null=True)
    address = models.TextField()
    ordered_at = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Placed')
  
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='orders', null=True)
    feedback = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(blank=True, null=True)
    feedback_at = models.DateTimeField(blank=True, null=True)
    
    def total_price(self):
        return self.product.price * self.quantity
    
class Category(models.Model):
    name = models.CharField(max_length=100)
 
    def __str__(self):
        return self.name



