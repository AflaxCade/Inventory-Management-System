from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	
	def __str__(self):
		return self.name

class Supplier(models.Model):
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