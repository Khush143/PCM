from django.contrib import admin
from .models import MyUser,Product, Category

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Product)
admin.site.register(Category)