from django.db import models
from datetime import date

TRANSMISSION_CHOICES = (
    ("AT", "Automática"),
    ("MT", "Manual"),
)

BODY_TYPE_CHOICES = (
    ("SD", "Sedán"),
    ("CN", "Camioneta"),
)

class Car(models.Model):
    brand = models.CharField("Marca", max_length=60)
    model = models.CharField("Modelo", max_length=80, blank=True)
    year = models.PositiveIntegerField("Año")  # usaremos año y calculamos edad
    transmission = models.CharField("Transmisión", max_length=2, choices=TRANSMISSION_CHOICES)
    body_type = models.CharField("Tipo", max_length=2, choices=BODY_TYPE_CHOICES, default="SD")
    color = models.CharField("Color", max_length=40)
    mileage_km = models.PositiveIntegerField("Kilometraje (km)", default=0)
    price_cop = models.DecimalField("Precio (COP)", max_digits=12, decimal_places=2)
    image = models.ImageField("Imagen del carro", upload_to="cars/", blank=True, null=True)

    is_active = models.BooleanField("Publicado", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Carro"
        verbose_name_plural = "Carros"

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}".strip()

    @property
    def age(self) -> int:
        """Edad calculada a partir del año."""
        current = date.today().year
        return max(0, current - (self.year or current))
