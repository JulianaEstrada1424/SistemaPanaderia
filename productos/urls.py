from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('productos/', views.ProductoListView.as_view(), name='producto_lista'),
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto_crear'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_eliminar'),
    path('productos/<int:pk>/toggle/', views.producto_toggle_estado, name='producto_toggle'),
]