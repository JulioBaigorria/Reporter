from django.http import JsonResponse
from django.http.response import HttpResponse
from django.views.generic import ListView
from django.views.generic import DetailView
from .utils import get_report_image
from Applications.Profile.models import Profile
from .models import Report
from .forms import ReportForm
# Create your views here.

class ReportListView(ListView):
    model = Report
    template_name = 'Report/home.html'
    context_object_name = 'lists'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'Report/detail.html'

def create_report_view(request):
    print('llego')
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