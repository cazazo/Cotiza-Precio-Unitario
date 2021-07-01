from django.db.models import Count
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from cotizacion.forms import PrecioUnitarioForm
from cotizacion.models import (Clientes, Cotizaciones, ItemCotiza, ManoObra,
                               Materiales, PreciosUnitarios, PuManoObra,
                               PuMaterial, Rendimientos)

from .forms import *

# Create your views here.


class Home(TemplateView):
    template_name = 'cotizacion/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['ct'] = Cotizaciones.objects.all().count()
        context['cl'] = Clientes.objects.all().count()
        context['m'] = Materiales.objects.all().count()
        context['mo'] = ManoObra.objects.all().count()
        context['rd'] = Rendimientos.objects.all().count()
        context['pu'] = PreciosUnitarios.objects.all().count()

        return context


class CreateMaterialView(CreateView):
    form_class = MaterialesForm
    model = Materiales
    redirect_field_name = 'cotizacion/materiales_detail.html'


class CreateClientView(CreateView):
    form_class = ClienteForm
    model = Clientes
    redirect_field_name = 'cotizacion/clientes_detail.html'


class CreateManoObraView(CreateView):
    form_class = ManoObraForm
    model = ManoObra
    redirect_field_name = 'cotizacion/manoobra_detail.html'


class CreateRendimientoView(CreateView):
    form_class = RendimientoForm
    model = Rendimientos
    redirect_field_name = 'cotizacion/rendimientos_detail.html'


class MaterialesListView(ListView):
    model = Materiales
    redirect_field_name = 'cotizacion/materiales_list.html'


class ClientesListView(ListView):
    model = Clientes
    redirect_field_name = 'cotizacion/cliente_list.html'


class ManoObraListView(ListView):
    model = ManoObra
    redirect_field_name = 'cotizacion/manoobra_list.html'


class RendimientoListView(ListView):
    model = Rendimientos
    redirect_field_name = 'cotizacion/rendimiento_list.html'


def PrecioUnitarioListView(request):
    pus_list = PreciosUnitarios.objects.all()
    return render(request, 'cotizacion/pu_list.html', {'pus_list': pus_list})


class CotizacionListView(ListView):
    model = Cotizaciones
    redirect_field_name = 'cotizacion/cotizacion_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cotizacion_list'] = Cotizaciones.objects.all()
        return context


def CotizacionDetailView(request, pk):
    cotiza_list = ItemCotiza.objects.filter(cotizacion_id=pk)
    cot_list = Cotizaciones.objects.filter(id=pk)
    context = {'cotiza_list': cotiza_list, 'cot_list': cot_list}
    return render(request, 'cotizacion/cotiza_list.html',
                  context=context)


class MaterialDetailView(DetailView):
    model = Materiales


def PrecioUnitarioDetailView(request, pk):
    pus_list = PreciosUnitarios.objects.filter(id=pk)
    pu_list = PuMaterial.objects.filter(puma_id=pk)
    mo_list = PuManoObra.objects.filter(pumo_id=pk)
    context = {'pu_list': pu_list, 'mo_list': mo_list, 'pus_list': pus_list}

    return render(request, 'cotizacion/pu_detail.html', context=context)


class ClienteDetailView(DetailView):
    model = Clientes


class ManoObraDetailView(DetailView):
    model = ManoObra


class RendimientoDetailView(DetailView):
    model = Rendimientos


class PrecioUnitarioFormView(CreateView):
    template_name = 'cotizacion/preciosunitarios_add.html'
    model = PreciosUnitarios
    form_class = PrecioUnitarioForm
    success_url = ''

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        pumaterial_form = PuMaterialFormSet()
        pumanoobra_form = PuManoobraFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  pumaterial_form=pumaterial_form,
                                  pumanoobra_form=pumanoobra_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        pumaterial_form = PuMaterialFormSet(self.request.POST)
        pumanoobra_form = PuManoobraFormSet(self.request.POST)
        if (form.is_valid() and pumaterial_form.is_valid() and
                pumanoobra_form.is_valid()):
            return self.form_valid(form, pumaterial_form, pumanoobra_form,)
        else:
            return self.form_invalid(form, pumaterial_form, pumanoobra_form,)

    def form_valid(self, form, pumaterial_form, pumanoobra_form):

        self.object = form.save()
        pumaterial_form.instance = self.object
        pumaterial_form.save()
        pumanoobra_form.instance = self.object
        pumanoobra_form.save()
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, pumaterial_form, pumanoobra_form):

        return self.render_to_response(
            self.get_context_data(form=form,
                                  pumaterial_form=pumaterial_form,
                                  pumanoobra_form=pumanoobra_form))


class CotizacionFormView(CreateView):
    template_name = 'cotizacion/cotizaciones_form.html'
    model = Cotizaciones
    form_class = CotizacionForm
    success_url = ''

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        puitemcotiza_form = PuItemCotizaFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  puitemcotiza_form=puitemcotiza_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        puitemcotiza_form = PuItemCotizaFormSet(self.request.POST)
        if (form.is_valid() and puitemcotiza_form.is_valid()):
            return self.form_valid(form, puitemcotiza_form)
        else:
            return self.form_invalid(form, puitemcotiza_form)

    def form_valid(self, form, puitemcotiza_form):
        self.object = form.save()
        puitemcotiza_form.instance = self.object
        puitemcotiza_form.save()
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, puitemcotiza_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  puitemcotiza_form=puitemcotiza_form))
