import csv
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from django.utils.dateparse import parse_date
from django.views.generic import ListView, DetailView, TemplateView
from django.template.loader import get_template
from Applications.Profile.models import Profile
from Applications.Sale.models import Sale, Position, CSV
from Applications.Product.models import Product
from Applications.Customer.models import Customer
from .models import Report
from .forms import ReportForm
from .utils import get_report_image
from xhtml2pdf import pisa

class ReportListView(ListView):
    model = Report
    template_name = 'Report/home.html'
    context_object_name = 'lists'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'Report/detail.html'

class UploadTemplateView(TemplateView):
    template_name = 'Report/from_file.html'

def csv_upload_view(request):
    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        #evitar subir un mismo archivo csv dos veces
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)
        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r') as file:
                reader = csv.reader(file)
                reader.__next__()
                for data in reader:
                    transaction_id = data[0]
                    product = data[1]
                    quantity = int(data[2])
                    customer = data[3]
                    date = parse_date(data[4])
                
                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    except Product.DoesNotExist:
                        product_obj = None

                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(product=product_obj,quantity=quantity,created=date)
                        sale_obj, _ = Sale.objects.get_or_create(transaction_id = transaction_id, customer = customer_obj, salesman = salesman_obj, created = date)
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()
            return JsonResponse({'ex': False})
        else:
            return JsonResponse({'ex': True})
    return HttpResponse()

def create_report_view(request):
    form = ReportForm(request.POST or None)
    if request.is_ajax():
        image = request.POST.get('image')
        img = get_report_image(image)
        author = Profile.objects.get(user=request.user)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.image = img
            instance.author = author
            instance.save()

        return HttpResponse(201)
    return JsonResponse({})


def render_pdf_view(request, pk):
    template_path = 'Report/pdf.html'
    #obj = Report.objects.get(id=pk)
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    
    # Para descargar
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # Para ver 
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response








    # def create_report_view(request):
#     print('llego')
#     if request.is_ajax():
#         name = request.POST.get('name')
#         remarks = request.POST.get('remarks')
        
#         image = request.POST.get('image')
#         img = get_report_image(image)
        
#         author = Profile.objects.get(user=request.user)
#         Report.objects.create(name=name, remarks=remarks, image=img, author=author, )
#         return JsonResponse({'msg': 'send'})
#     return JsonResponse({})