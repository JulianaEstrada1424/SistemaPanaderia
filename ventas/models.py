from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto  # Importamos el modelo de productos

class Venta(models.Model):
    ESTADO_CHOICES = (
        ('COMPLETADA', 'Completada'),
        ('CORREGIDA', 'Corregida'),
        ('ANULADA', 'Anulada'),
    )
    
    cajero = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='COMPLETADA')
    motivo_anulacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Venta #{self.id} - ${self.total} ({self.estado})"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

class HistorialModificacionVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='historial', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=50)  # Ejemplo: "ANULACION", "CORRECCION"
    motivo = models.TextField()

    def __str__(self):
        return f"{self.accion} en Venta #{self.venta.id} por {self.usuario.username}"