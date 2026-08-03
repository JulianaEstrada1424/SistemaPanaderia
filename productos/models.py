from django.db import models


class Categoria(models.Model):
    """
    Representa una categoría de productos de la panadería
    (ej: Panes, Pasteles, Galletas, Bebidas).
    """
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