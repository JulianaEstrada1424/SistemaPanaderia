
# Register your models here.
from django.contrib import admin
from .models import Venta, DetalleVenta, HistorialModificacionVenta

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cajero', 'fecha', 'total', 'estado')
    list_filter = ('estado', 'fecha')
    inlines = [DetalleVentaInline]

@admin.register(HistorialModificacionVenta)
class HistorialModificacionVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'usuario', 'accion', 'fecha')
    list_filter = ('accion', 'fecha')