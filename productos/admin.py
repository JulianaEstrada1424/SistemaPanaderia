from django.contrib import admin
from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'fecha_creacion')
    list_filter = ('estado',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'categoria')
    search_fields = ('nombre',)
    ordering = ('nombre',)