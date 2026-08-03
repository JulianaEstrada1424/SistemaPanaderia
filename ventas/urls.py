# ventas/urls.py
from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.HistorialVentasView.as_view(), name='historial'),
    path('nueva/', views.CrearVentaView.as_view(), name='crear_venta'),
    path('anular/<int:venta_id>/', views.anular_venta_view, name='anular_venta'),
]