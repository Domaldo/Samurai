from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, ListView, DetailView, RedirectView
from .forms import CreateNewLocksmith, LookForLocksmith, ContractForm
from .models import Cerrajero, Rating, Job


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
        serviceType, serviceObject, city = self.request.GET.values()
        self.request.session['serviceType'] = serviceType
        self.request.session['serviceObject'] = serviceObject
        self.request.session['serviceObject'] = serviceObject
        d = {}
        # Si viene el ID de la ciudad agrego ese campo a los filtros
        if city:
            d = {"city__pk": city}
        # Consulta a usuarios donde filtra sus campos basados en los filtros enviados por GET
        # Hace Join con la tabla cerrajeros, con rating y con ciudad
        objects_filter = Cerrajero.objects.filter(serviceType__contains=serviceType,
                                                  serviceObject__contains=serviceObject,
                                                  **d).annotate(
            avg=Avg('rating__rate', output_field=models.DecimalField())).order_by('-avg')
        # Devuelve los registros filtrados
        return objects_filter


class l_data(DetailView, LoginRequiredMixin):
    template_name = "main/locksmith-data.html"
    model = Cerrajero


class Vote(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        rate, pk = self.request.GET.values()
        Rating.objects.create(cerrajero=Cerrajero.objects.get(pk=pk), rate=rate)
        return super().get_redirect_url(*args, **kwargs)


class Contract(LoginRequiredMixin, CreateView):
    template_name = 'main/job.html'
    form_class = ContractForm
    model = Job
    success_url = '/'

    def get_initial(self):
        initial = super().get_initial()
        initial['request'] = self.request
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        date_ = form.instance.date
        cerr = Cerrajero.objects.get(pk=self.kwargs.get('pk'))
        dispo = cerr.available.filter(end_date__gte=date_, start_date__lte=date_).exists()
        if not dispo:
            form.add_error('__all__', "{}, no esta disponible".format(date_))
            return super().form_invalid(form)
        form.instance.cerrajero = cerr
        return super().form_valid(form)


class Contract_List(ListView, LoginRequiredMixin):
    template_name = "main/job-list.html"

    def get_queryset(self):
        return Job.objects.filter(cerrajero__user=self.request.user)


class Contract_Status(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        pk = kwargs.get('pk')
        status = kwargs.get('status')
        job = Job.objects.get(pk=pk)
        job.status = status
        job.save()
        return super().get_redirect_url(*args, **kwargs)
