import pandas as pd
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.utils import timezone
from .forms import SalesSearchForm
from .models import Sale


def home_view(request):
    sales_df = None
    positions_df = None
    form = SalesSearchForm(request.POST or None)
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        
        sales_qs = Sale.objects.filter(created__date__lte=date_to,
                                       created__date__gte=date_from)
        if len(sales_qs) > 0:
            sales_df = pd.DataFrame(sales_qs.values())
            sales_df = sales_df.to_html()
            positions_data = []
            
            for sale in sales_qs:
                for pos in sale.get_positions():
                    obj= {
                        'position_id': pos.id,
                        'sale_id': pos.get_sales_id(),
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                    }
                    positions_data.append(obj)
            positions_df = pd.DataFrame(positions_data)
            positions_df = positions_df.to_html()
            print(positions_df)
        else:
            print("No data")

    context = {
        'form': form,
        'sales_df': sales_df,
        'positions_df': positions_df,
    }
    return render(request, 'Sale/home.html', context)


class SaleListView(ListView):
    model = Sale
    template_name = 'Sale/main.html'
    context_object_name = 'sales'


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'Sale/detail.html'
    context_object_name = 'details'
