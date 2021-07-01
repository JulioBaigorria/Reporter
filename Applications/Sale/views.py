import pandas as pd
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from Applications.Report.forms import ReportForm
from .forms import SalesSearchForm
from .models import Sale
from .utils import get_chart, get_customer_from_id, get_salesman_from_id
#from django.utils import timezone

def home_view(request):
    sales_df = None
    positions_df = None
    merged_df = None
    merged_df_group = None
    chart = None
    search_form = SalesSearchForm(request.POST or None)
    report_form = ReportForm()
    result_type = None
    no_data = None
    
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        result_type = request.POST.get('result_type')
        
        sales_qs = Sale.objects.filter(created__date__lte=date_to,
                                       created__date__gte=date_from)
        #print(sales_qs)
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
            #print(sales_df.dtypes)
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
            merged_df_group = merged_df.groupby('transaction_id', as_index=False)['total_price'].agg('sum')
            
            #se llama a la funcion de util
            chart = get_chart(chart_type, sales_df, result_type)
            
            #convertir los dataframes en html
            positions_df = positions_df.to_html()
            #hago sort por sales_df['total_price] y despues paso a html
            sales_df = sales_df.sort_values('total_price', ascending=False)
            sales_json = sales_df.to_dict()
            sales_df = sales_df.to_html()
            merged_df = merged_df.to_html()
            print(sales_json)
        else:
            #se puede utilizar un true y false pero es preferible asi
            no_data = 'No hay datos en este rango de fecha'

    context = {
        'search_form': search_form,
        'report_form': report_form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'merged_df_group': merged_df_group,
        'chart':chart,
        'no_data':no_data,
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
