from django.views.generic import ListView 
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CreateProductForm
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'Product/main.html'

class ProductCreateView(CreateView):
    model = Product
    form_class = CreateProductForm
    template_name = 'Product/create.html'
    success_url = '/products/'

