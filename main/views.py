from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, ListView, DetailView, RedirectView
from django.db import models
from .forms import CreateNewLocksmith, LookForLocksmith
from .models import Cerrajero, Rating


# Create your views here.

def index(response, id):
    cj = Cerrajero.objects.get(id=id)
    return render(response, "main/locksmith-list.html", {"cj": cj})


class Home(TemplateView):
    template_name = "main/home.html"


class l_create(LoginRequiredMixin, CreateView):
    model = Cerrajero
    template_name = 'main/locksmith-create.html'
    success_url = '/'
    form_class = CreateNewLocksmith

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def l_edit(response):
    return render(response, "main/locksmith-edit.html", {})


def l_search(response):
    form = LookForLocksmith()
    return render(response, "main/locksmith-search.html/", {"form": form})


class l_list(ListView, LoginRequiredMixin):
    template_name = "main/locksmith-list.html"
    """
        Metodo que devuelve y filtra todos los Usuarios 
        que son cajeros ordenados por el promedio de rating
    """

    def get_queryset(self):
        # Recogo la lista de filtros que vienen por la URL
        # serviceType, serviceObject, serviceUrgency, serviceIntent, city = self.request.GET.values()
        serviceType, serviceObject, serviceUrgency, serviceIntent = self.request.GET.values()
        # d = {}
        # Si viene el ID de la ciudad agrego ese campo a los filtros
        # if city:
            # d = {"cerrajero__ciudad__pk": city}
        # Consulta a usuarios donde filtra sus campos basados en los filtros enviados por GET
        # Hace Join con la tabla cerrajeros, con rating y con ciudad
        objects_filter = User.objects.filter(cerrajero__serviceType__contains=serviceType,
                                             cerrajero__serviceObject__contains=serviceObject,
                                             cerrajero__serviceIntent__contains=serviceIntent,
                                             cerrajero__serviceUrgency__contains=serviceUrgency
                                             #,**d
                                             ).annotate(
            avg=Avg('rating__rate', output_field=models.DecimalField())).order_by('-avg')
        # Devuelve los registros filtrados
        return objects_filter


class l_data(DetailView, LoginRequiredMixin):
    template_name = "main/locksmith-data.html"
    model = Cerrajero


class Vote(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        rate, pk = self.request.GET.values()
        Rating.objects.create(cerrajero=User.objects.get(pk=pk), rate=rate)
        return super().get_redirect_url(*args, **kwargs)
