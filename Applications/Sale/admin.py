from django.contrib import admin
from .models import Position, Sale, CSV

# Register your models here.

@admin.register(Position)
class Admin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price',)
    list_filter = ('product', 'quantity', 'price',)

@admin.register(Sale)
class Admin(admin.ModelAdmin):
    list_display = ('transaction_id', 'total_price', 'customer','created',)
    list_filter = ('positions', 'total_price', 'customer','salesman',)

@admin.register(CSV)
class Admin(admin.ModelAdmin):
    list_display = ('file_name',)
    list_filter = ('file_name', )
