from django.contrib import admin
from .models import Product
# Register your models here.

@admin.register(Product)
class Admin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name','price',)