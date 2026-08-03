# Register your models here.
from django.contrib import admin
from .models import Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'fecha_creacion')
    list_filter = ('estado',)
    search_fields = ('nombre',)
    ordering = ('nombre',)