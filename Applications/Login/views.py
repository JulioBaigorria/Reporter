from django.views.generic import FormView, TemplateView, RedirectView

# Authentication imports
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm

from django.urls import reverse_lazy

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "Login/login.html"
    success_url =  reverse_lazy("Sale:home")

    def dispatch(self, request, *args, **kwargs):
        print(self.request.user)
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        print("Hola: ", self.request.user)
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        print("Nos re vimos")
        return super(LogoutView, self).get(request, *args, **kwargs)