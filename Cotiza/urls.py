"""Cotiza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cotizacion.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    #     materiales urls:
    path('materiales/', MaterialesListView.as_view(), name='materiales_list'),
    path('materiales/new/', CreateMaterialView.as_view(), name='materiales_new'),
    path('material/<int:pk>',
         MaterialDetailView.as_view(), name='material_detail'),

    #     Clientes urls:
    path('clientes/', ClientesListView.as_view(), name='clientes_list'),
    path('clientes/new/', CreateClientView.as_view(), name='clientes_new'),
    path('cliente/<int:pk>',
         ClienteDetailView.as_view(), name='cliente_detail'),

    #     Mano de Obra urls:
    path('manoobra/', ManoObraListView.as_view(), name='manoobra_list'),
    path('manoobra/new/', CreateManoObraView.as_view(), name='mo_new'),
    path('mo/<int:pk>',
         ManoObraDetailView.as_view(), name='mo_detail'),

    #     Rendimiento urls:
    path('rendimientos/', RendimientoListView.as_view(), name='rendimientos_list'),
    path('rendimientos/new/', CreateRendimientoView.as_view(),
         name='rendimientos_new'),
    path('rendimiento/<int:pk>',
         RendimientoDetailView.as_view(), name='rendimiento_detail'),

    #     Cotizaciones urls:
    path('cotizaciones/', CotizacionListView.as_view(), name='cotizacion_list'),
    path('cotizaciones/new/', CotizacionFormView.as_view(),
         name='cotizaciones_new'),
    path('cotizacion/<int:pk>', CotizacionDetailView, name='cotizacion_detail'),

    #     Precios Unitarios urls:
    path('pu/', PrecioUnitarioListView, name='pu_list'),
    path('pu/<int:pk>', PrecioUnitarioDetailView, name='pu_detail'),
    path('pu/new/', PrecioUnitarioFormView.as_view(), name='pu_new'),
]
