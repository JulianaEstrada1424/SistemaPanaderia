from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ProductoForm
from .models import Categoria, Producto


def inicio(request):
    """Página informativa: resumen de categorías y productos destacados."""
    categorias = Categoria.objects.filter(estado=True)[:6]
    productos_destacados = Producto.objects.filter(estado=True)[:6]
    return render(request, "productos/inicio.html", {
        "categorias": categorias,
        "productos_destacados": productos_destacados,
    })


class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_lista.html'
    context_object_name = 'productos'
    paginate_by = 10

    def get_queryset(self):
        queryset = Producto.objects.select_related('categoria').all()
        buscar = self.request.GET.get('buscar')
        categoria_id = self.request.GET.get('categoria')
        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.filter(estado=True)
        return context


class ProductoCreateView(SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto_lista')
    success_message = "Producto '%(nombre)s' creado correctamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Producto'
        return context


class ProductoUpdateView(SuccessMessageMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/producto_form.html'
    success_url = reverse_lazy('producto_lista')
    success_message = "Producto '%(nombre)s' actualizado correctamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Producto'
        return context


class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_lista')

    def form_valid(self, form):
        messages.success(self.request, f"Producto '{self.object.nombre}' eliminado correctamente.")
        return super().form_valid(form)


def producto_toggle_estado(request, pk):
    """Da de baja/alta un producto sin eliminarlo (baja lógica) con un solo clic."""
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.estado = not producto.estado
        producto.save(update_fields=['estado'])
        estado_txt = "activado" if producto.estado else "desactivado"
        messages.success(request, f"Producto '{producto.nombre}' {estado_txt}.")
    return redirect('producto_lista')