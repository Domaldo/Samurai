from django.views.generic import CreateView
from .forms import RegisterForm


# Create your views here.

class register(CreateView):
    template_name = "register/register.html"
    form_class = RegisterForm
    success_url = '/login/'
