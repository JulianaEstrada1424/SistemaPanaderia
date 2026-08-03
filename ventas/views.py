from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Venta, DetalleVenta, HistorialModificacionVenta
from productos.models import Producto

class HistorialVentasView(ListView):
    model = Venta
    template_name = 'ventas/historial.html'
    context_object_name = 'ventas'
    paginate_by = 10

    def get_queryset(self):
        # Ordenar por las más recientes
        return Venta.objects.all().order_by('-fecha')

class CrearVentaView(TemplateView):
    template_name = 'ventas/nueva_venta.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos solo los productos activos y con stock
        context['productos'] = Producto.objects.filter(activo=True)
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Recibimos los productos seleccionados en formato JSON desde el frontend
        data = json.loads(request.body)
        items = data.get('items', [])
        
        if not items:
            return JsonResponse({'error': 'No hay productos en la venta'}, status=400)

        # 1. Crear cabecera de la Venta
        venta = Venta.objects.create(
            cajero=request.user,
            total=0.00
        )

        total_venta = 0

        # 2. Registrar cada producto y descontar stock
        for item in items:
            producto = get_object_or_404(Producto, id=item['id'])
            cantidad = int(item['cantidad'])

            if producto.stock < cantidad:
                # Al lanzar una excepción dentro de transaction.atomic,
                # se deshacen todos los cambios automáticamente (rollback)
                raise ValueError(f"Stock insuficiente para {producto.nombre}")

            subtotal = producto.precio * cantidad
            total_venta += subtotal

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio,
                subtotal=subtotal
            )

            # Descontar del inventario
            producto.stock -= cantidad
            producto.save()

        # 3. Actualizar total final de la venta
        venta.total = total_venta
        venta.save()

        return JsonResponse({'status': 'ok', 'venta_id': venta.id})

@transaction.atomic
def anular_venta_view(request, pk):
    if request.method == 'POST':
        venta = get_object_or_404(Venta, pk=pk)
        
        if venta.estado == 'ANULADA':
            messages.error(request, "Esta venta ya se encuentra anulada.")
            return redirect('ventas:historial')

        motivo = request.POST.get('motivo', 'Anulación solicitada por el usuario')

        # 1. Devolver el stock a cada producto
        for detalle in venta.detalles.all():
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save()

        # 2. Cambiar estado de la venta
        venta.estado = 'ANULADA'
        venta.motivo_anulacion = motivo
        venta.save()

        # 3. Guardar registro en la tabla de auditoría
        HistorialModificacionVenta.objects.create(
            venta=venta,
            usuario=request.user,
            accion='ANULACION',
            motivo=motivo
        )

        messages.success(request, f"La venta #{venta.id} ha sido anulada y el stock devuelto.")
        return redirect('ventas:historial')