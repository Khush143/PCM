from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Admin', 'Admin User'),
        ('normal', 'Normal User'),
    )

    CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=CHOICES, blank=True, null=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='normal')
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    Admin=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    last_price_update_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', default="")   
    def __str__(self):
        return self.Admin.first_name+" - "+self.name