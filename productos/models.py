from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Categoria(models.Model):
    # ... (tu clase Categoria del Paso 1, sin cambios) ...
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(
        default=True,
        help_text="Desmarca para desactivar la categoría sin eliminarla (baja lógica)."
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Producto del inventario de la panadería.
    Nombres de campos pensados para integrarse con:
    - Carga masiva CSV (columnas: nombre, categoria, precio, stock)
    - Predicción de demanda (usa stock, precio, categoria, fecha_creacion)
    - Ventas (usa precio, stock para descontar al vender)
    """
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name="Categoría"
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Precio de venta en dólares."
    )
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Unidades disponibles en inventario."
    )
    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True
    )
    estado = models.BooleanField(
        default=True,
        help_text="Desmarca para dar de baja el producto sin eliminarlo (baja lógica)."
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('producto_lista')

    @property
    def stock_bajo(self):
        """Útil para el módulo de predicción de demanda / alertas."""
        return self.stock <= 5