from django.contrib import admin
from django.apps import apps
from cotizacion.models import *

# Register your models here.
admin.site.register(apps.all_models['cotizacion'].values())
