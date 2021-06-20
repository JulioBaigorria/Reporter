import uuid
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from Applications.Customer.models import Customer
from Applications.Profile.models import Profile

def generate_code():
    code = uuid.uuid4()
    code_mod = str(code).replace('-', '')[:12]
    return code_mod

def get_salesman_from_id(val):
    #se obtiene __str__ por medio del get
    salesman = Profile.objects.get(id=val)
    return salesman

def get_customer_from_id(val):
    #se obtiene __str__ por medio del get
    customer = Customer.objects.get(id=val)
    return customer

def get_graph():
    #https://docs.python.org/3.8/library/io.html#io.IOBase.seek
    #se crea un buffer BytesIO ver: tream
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

def get_chart(chart_type, data, **kwargs):
    #usar siempre para cambiar el modulo del kernel
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4))
    if chart_type == '#1':
        plt.bar(data['transaction_id'], data['price'])
    elif chart_type == '#2':
        labels = kwargs.get('labels')
        plt.pie(data = data, x='price', labels=labels)
    elif chart_type == '#3':
        plt.plot(data['transaction_id'], data['price'])
    plt.tight_layout()
    chart = get_graph()
    return chart