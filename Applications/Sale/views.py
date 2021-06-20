import pandas as pd
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.utils import timezone
from .forms import SalesSearchForm
from .models import Sale
from .utils import get_chart, get_customer_from_id, get_salesman_from_id


def home_view(request):
    sales_df = None
    positions_df = None
    merged_df = None
    chart = None
    form = SalesSearchForm(request.POST or None)
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        
        sales_qs = Sale.objects.filter(created__date__lte=date_to,
                                       created__date__gte=date_from)
        if len(sales_qs) > 0:
            sales_df = pd.DataFrame(sales_qs.values())
            
            #encuentra los nombres por id
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            #los reemplaza en el dataframe
            sales_df.rename({'customer_id':'customer','salesman_id':'salesman', 'id': 'sales_id'}, axis=1, inplace=True)
            #formateando la fecha
            sales_df['created'] = sales_df['created'].apply(lambda x:x.strftime('%d/%m/%y'))
            sales_df['updated'] = sales_df['updated'].apply(lambda x:x.strftime('%d/%m/%y'))
            
            positions_data = []
            for sale in sales_qs:
                for pos in sale.get_positions():
                    obj= {
                        'sales_id': pos.get_sales_id(),
                        'position_id': pos.id,
                        'product': pos.product.name,
                        'quantity': pos.quantity,
                        'price': pos.price,
                    }
                    positions_data.append(obj)
            
            positions_df = pd.DataFrame(positions_data)
            #merge de los dos dataframes
            merged_df = pd.merge(sales_df, positions_df, on="sales_id")
            merged_df_group = merged_df.groupby('transaction_id', as_index=False).agg('sum')
            
            #se llama a la funcion de util
            chart = get_chart(chart_type, merged_df, labels=merged_df['transaction_id'].values)
            
            #convertir los dataframes en html
            positions_df = positions_df.to_html()
            sales_df = sales_df.to_html()
            merged_df = merged_df.to_html()
            merged_df_group = merged_df_group.to_html()
        else:
            print("No data")

    context = {
        'form': form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'merged_df_group':merged_df_group,
        'chart':chart,
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
