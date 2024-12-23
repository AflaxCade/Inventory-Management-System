from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from PIL import Image


class Customer(models.Model):
    """
    Model to represent a Customer.
    """
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.name if self.name else "Unnamed Customer"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.profile_pic:
            img = Image.open(self.profile_pic.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_pic.path)


class Supplier(models.Model):
    """
    Model to represent a Supplier.
    """
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex='^[0-9+\-]+$',  # Allows digits, plus, and minus symbols
                message='Phone number must be numeric and can include +, - symbols',
                code='invalid_phone_number'
            ),
        ]
    )
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    """
    Model to represent a Category.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    """
    Model to represent a Product.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    """
    Model to represent an Order.
    """
    STATUS = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=200, choices=STATUS, default='Pending')
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Order of {self.quantity} {self.product.name}(s) by {self.customer.name} on {self.date_created}'
    

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    invoice_number = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.customer.name}"