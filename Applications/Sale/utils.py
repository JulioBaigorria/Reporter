import uuid
import base64
import seaborn as sns
from io import BytesIO
import matplotlib.pyplot as plt
from Applications.Customer.models import Customer
from Applications.Profile.models import Profile

def generate_code():
    code = uuid.uuid4()
    code_mod = str(code).replace('-', '')[:12]
    return code_mod

    #obtener los nombres a partit del id
def get_salesman_from_id(val):
    #se obtiene __str__ por medio del get
    salesman = Profile.objects.get(id=val)
    return salesman

    #obtener los nombres por id
def get_customer_from_id(val):
    #se obtiene __str__ por medio del get
    customer = Customer.objects.get(id=val)
    return customer

def get_graph():
    #https://docs.python.org/3.8/library/io.html#io.IOBase.seek
    #se crea un buffer BytesIO ver: stream
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    #se cambia la posicion del stream a entrada
    buffer.seek(0)
    image_png = buffer.getvalue()
    #https://contenttu.com/blog/seo/cuales-son-las-etiquetas-para-seo-mas-importantes
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    #se cierra el stream
    buffer.close()
    return graph

    #filtro para mostrar chart

def get_key(res_by):
    if res_by =='#1':
        key = 'created'
    else:
        key = 'transaction_id'
    return key

def get_chart(chart_type, data, results_by, **kwargs):
    #usar siempre para cambiar el modulo del kernel
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4))
    key = get_key(results_by)
    grouped = data.groupby(key, as_index=False)['total_price'].agg('sum')
    if chart_type == '#1':
        #se usa seaborn para esta
        #plt.bar(grouped[key], grouped['total_price'])
       #https://seaborn.pydata.org/generated/seaborn.barplot.html
        sns.barplot(x=key, y='total_price', data=grouped)
    elif chart_type == '#2':
        labels = kwargs.get('labels')
        plt.pie(data = grouped, x='total_price', labels=grouped[key].values)
    elif chart_type == '#3':
        #pueden haber markers 'x' u 'o'
        plt.plot(grouped[key], grouped['total_price'], color='red', marker='x', linestyle='dashed')
    plt.tight_layout()
    chart = get_graph()
    return chart