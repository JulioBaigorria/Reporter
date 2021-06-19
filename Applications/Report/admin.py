from django.contrib import admin
from .models import Report
# Register your models here.

@admin.register(Report)
class Admin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('name',)