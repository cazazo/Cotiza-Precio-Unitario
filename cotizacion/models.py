from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.urls import reverse
from pandas.core.aggregation import aggregate


def validate_s(value):
    try:
        return round(float(value), 2)
    except:
        raise ValidationError(
            ('%(value)s is not an integer or a float  number'),
            params={'value': value},
        )


class Materiales (models.Model):
    UNIDADES_CHOICES = [
        ('PZA', 'PIEZA'),
        ('UND', 'UNIDAD'),
        ('M', 'METRO LINEAR'),
        ('KG', 'KILOGRAMO'),
    ]
    material_nombre = models.CharField('Nombre', max_length=120)
    marca = models.CharField('Marca', max_length=120)
    descripcion = models.CharField('Descripción', max_length=300)
    precio = models.FloatField('Precio')
    unidad = models.CharField('Unidad',
                              max_length=3, choices=UNIDADES_CHOICES, default='PZA')

    class Meta:
        ordering = ['material_nombre']

    def __str__(self):
        return self.material_nombre+' ' + self.marca + ' ' + self.descripcion + ' '+self.unidad

    def get_absolute_url(self):
        return reverse('material_detail', kwargs={'pk': self.pk})


class Clientes(models.Model):
    nombre = models.CharField('Nombre', max_length=200)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('cliente_detail', kwargs={'pk': self.pk})


class ManoObra(models.Model):
    cargo = models.CharField('Cargo', max_length=150, unique=True)
    salario = models.FloatField('Salario')

    class Meta:
        ordering = ['cargo']

    def __str__(self):
        return self.cargo

    def get_absolute_url(self):
        return reverse('mo_detail', kwargs={'pk': self.pk})


# Posibilidad de desarrollo --> análisis de rendimientos


class Rendimientos(models.Model):
    nombre = models.CharField('Nombre', max_length=120, unique=True)
    descripcion = models.CharField('Descripción', max_length=200)
    unidades_jornal = models.FloatField(default=1.0)

    class Meta():
        ordering = ['nombre']

    def __str__(self):
        return self.nombre + " - " + self.descripcion

    def get_absolute_url(self):
        return reverse('rendimiento_detail', kwargs={'pk': self.pk})


class Variables(models.Model):
    utilidad = models.FloatField(default=0.15)
    iva = models.FloatField(default=1.1494)
    gastos_admin = models.FloatField(
        default=0.10)
    herramientas = models.FloatField(
        default=0.02)
    seguridad = models.FloatField(
        default=0.04)

    def __str__(self):
        return ("Utilidad: "+str(self.utilidad)+", IVA: "+str(self.iva)
                + ", generales & Administrativos: "+str(self.gastos_admin))


# implementación futura - discriminar los materiales


class PreciosUnitarios(models.Model):
    rendimiento = models.ForeignKey(
        Rendimientos, on_delete=models.CASCADE, related_name='rendimiento')
    mano_obra = models.ManyToManyField(
        ManoObra, through='PuManoObra', related_name='mano_obra')
    material_id = models.ManyToManyField(
        Materiales, through='PuMaterial', related_name='material')
    valor_mo = models.FloatField(
        blank=True, null=True)
    valor_material = models.FloatField(
        blank=True, null=True)

    def __str__(self) -> str:
        return self.rendimiento.nombre

    def get_total(self):
        return self.valor_mo + self.valor_material

    def get_absolute_url(self):
        return reverse('pu_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.id:
            pk = self.id
            v = Variables.objects.get(pk=2)
            rm = (self.rendimiento.unidades_jornal)
            jc = ManoObra.objects.get(cargo='Jefe de Cuadrilla')
            pu_m = PuMaterial.objects.filter(puma_id=pk)
            pu_mo = PuManoObra.objects.filter(pumo_id=pk)
            tm = pu_m.aggregate(Sum('subtotal'))['subtotal__sum']
            tmo = pu_mo.aggregate(Sum('mo_subtotal'))['mo_subtotal__sum']
            tmo = (tmo + ((jc.salario*8/208) * 0.10))/rm
            total_herramientas = tmo * float(v.herramientas)
            total_seguridad = tmo * float(v.seguridad)
            subtotal = tm + tmo + total_herramientas + total_seguridad
            total = subtotal / float(1 - v.gastos_admin)
            total = total/float(1-v.utilidad)
            total = total*float(v.iva)
            self.valor_mo = round(total * (tmo/subtotal), 2)
            self.valor_material = round(total * (tm/subtotal), 2)

            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


class PuManoObra(models.Model):
    manoobra_id = models.ForeignKey(
        ManoObra, on_delete=models.CASCADE, related_name="manoobra_id")
    pumo_id = models.ForeignKey(
        PreciosUnitarios, on_delete=models.CASCADE, related_name='pumo_id', null=True, blank=True)
    valor_jornal = models.FloatField(
        null=True, blank=True)
    mo_subtotal = models.FloatField(
        null=True, blank=True)
    ctd = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.pumo_id.rendimiento.nombre + ", "+self.manoobra_id.cargo

    def save(self, *args, **kwargs):
        vj = round(self.manoobra_id.salario/26, 2)
        self.valor_jornal = vj
        self.mo_subtotal = round(self.ctd*vj, 2)
        super().save(*args, **kwargs)


class PuMaterial(models.Model):
    material_id = models.ForeignKey(
        Materiales, on_delete=models.CASCADE, related_name='material_id')
    puma_id = models.ForeignKey(
        PreciosUnitarios, on_delete=models.CASCADE, related_name='puma_id', null=True, blank=True)
    cantidad = models.FloatField(
        default=1.00)
    subtotal = models.FloatField(
        null=True, blank=True)

    class Meta():
        unique_together = [['material_id', 'puma_id']]

    def __str__(self) -> str:
        return self.puma_id.rendimiento.nombre + ", Material: "+self.material_id.material_nombre

    def save(self, *args, **kwargs):
        self.subtotal = round(self.material_id.precio * self.cantidad, 2)
        super().save(*args, **kwargs)


class Cotizaciones(models.Model):
    cliente_id = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    pu_id = models.ManyToManyField(PreciosUnitarios, through='ItemCotiza')
    valor_mo = models.FloatField(
        blank=True, null=True)
    valor_materiales = models.FloatField(blank=True, null=True)
    creado_en = models.DateTimeField(default=timezone.now)

    class Meta():
        ordering = ['-creado_en']

    def get_valor_total(self):
        return self.valor_mo + self.valor_materiales

    def get_absolute_url(self):
        return reverse('cotizacion_detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return "Cotización #: " + str(self.id) + " - Cliente: " + self.cliente_id.nombre

    def save(self, *args, **kwargs):
        if self.id:
            ic = ItemCotiza.objects.filter(cotizacion_id=self.id)
            tm = ic.aggregate(Sum('valor_material'))['valor_material__sum']
            tmo = ic.aggregate(Sum('valor_mo'))['valor_mo__sum']
            self.valor_materiales = round(tm, 2)
            self.valor_mo = round(tmo, 2)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


class ItemCotiza(models.Model):
    pu_id = models.ForeignKey(
        PreciosUnitarios, on_delete=models.CASCADE)
    cotizacion_id = models.ForeignKey(
        Cotizaciones, related_name='items', on_delete=models.CASCADE)
    cantidad = models.FloatField(
        default=1.00)
    valor_material = models.FloatField(
        blank=True, null=True)
    valor_mo = models.FloatField(
        blank=True, null=True)

    class Meta():
        unique_together = [['cotizacion_id', 'pu_id']]

    def __str__(self):
        return str(self.cotizacion_id)+self.pu_id.rendimiento.nombre+" Cantidad: "+str(self.cantidad)

    def get_total(self):
        return (self.valor_mo + self.valor_material)

    def save(self, *args, **kwargs):
        self.valor_material = round(
            self.pu_id.valor_material * self.cantidad, 2)
        self.valor_mo = round(self.pu_id.valor_mo * self.cantidad, 2)
        super().save(*args, **kwargs)
