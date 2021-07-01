from django import forms
from django.forms.models import inlineformset_factory
from django.db.models import fields
from spyder import widgets

from cotizacion.models import *


class MaterialesForm(forms.ModelForm):
    class Meta():
        model = Materiales
        fields = '__all__'
        labels = {
            'material_nombre': '',
            'marca': '',
            'descripcion': '',
            'precio': '',
            'unidad': '',
        }
        widgets = {
            'material_nombre': forms.TextInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Material - Nome'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la Marca'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'precio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Precio del Material'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta():
        model = Clientes
        fields = '__all__'
        widgets = {'nombre': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Ingrese Nombre'}), }


class ManoObraForm(forms.ModelForm):
    class Meta():
        model = ManoObra
        fields = ('cargo', 'salario')
        labels = {'cargo': '', 'salario': ''}
        widgets = {
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo'}),
            'salario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Salario'}),
        }


class RendimientoForm(forms.ModelForm):
    class Meta():
        model = Rendimientos
        fields = '__all__'
        labels = {'nombre': '', 'descripcion': '', 'unidades_jornal': ''}
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'unidades_jornal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Unidades/jornal'}),
        }


class CotizacionForm(forms.ModelForm):
    class Meta():
        model = Cotizaciones
        fields = ['cliente_id',
                  # 'valor_mo',
                  # 'valor_materiales'
                  ]
        labels = {'cliente_id': 'Cliente',
                  # 'valor_mo': '',
                  # 'valor_materiales': ''
                  }
        widgets = {
            'cliente_id': forms.Select(attrs={'class': 'form-control'}),
            'valor_mo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Precio del Material'}),
            'valor_materiales': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Precio del Material'})}


class ItemCotizaForm(forms.ModelForm):
    class Meta():
        model = ItemCotiza
        fields = '__all__'


PuItemCotizaFormSet = inlineformset_factory(
    Cotizaciones, ItemCotiza, fields=(
        'pu_id', 'cotizacion_id', 'cantidad'),
    widgets={
        'pu_id': forms.Select(attrs={'class': 'form-control'}),
        'cotizacion_id': forms.Select(attrs={'class': 'form-control'}),
        'cantidad': forms.TextInput(attrs={'class': 'form-control'})
    },
    labels={
        'pu_id': 'Material',
        'cotizacion_id': 'Cotización',
        'cantidad': 'Cantidad'
    }, can_delete=False, extra=10)


class VariablesForm(forms.ModelForm):
    class Meta():
        model = Variables
        fields = '__all__'


# PRECIO UNITARIO


class PrecioUnitarioForm(forms.ModelForm):
    class Meta():
        model = PreciosUnitarios
        fields = ('rendimiento',
                  #   'mano_obra',
                  #   'material_id',
                  #   'valor_mo',
                  #   'valor_material'
                  )
        labels = {
            'rendimiento': 'Selecionar Rendimiento',
            'mano_obra': 'Selecionar Mano de Obra',
            'material_id': '',
            'valor_mo': '',
            'valor_material': '',
        }
        widgets = {
            'rendimiento': forms.Select(attrs={'class': 'form-control'}),
            'mano_obra': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'material_id': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'valor_mo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Precio del Material'}),
            'valor_material': forms.TextInput(attrs={'class': 'form-control'}),
        }


PuMaterialFormSet = inlineformset_factory(
    PreciosUnitarios, PuMaterial, fields=(
        'material_id', 'puma_id', 'cantidad'),
    widgets={
        'material_id': forms.Select(attrs={'class': 'form-control'}),
        'puma_id': forms.Select(attrs={'class': 'form-control'}),
        'cantidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'})
    },
    labels={
        'material_id': 'Material',
        'puma_id': 'id',
        'cantidad': ''
    }, can_delete=False, extra=10)


PuManoobraFormSet = inlineformset_factory(
    PreciosUnitarios, PuManoObra, fields=('manoobra_id', 'pumo_id', 'ctd'),
    widgets={
        'manoobra_id': forms.Select(attrs={'class': 'form-control'}),
        'pumo_id': forms.Select(attrs={'class': 'form-control'}),
        'ctd': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'})
    },
    labels={
        'manoobra_id': 'Mano Obra',
        'pumo_id': 'id',
        'ctd': ''
    }, can_delete=False)
