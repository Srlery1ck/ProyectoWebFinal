from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "age", "transmission", "color", "mileage_km", "precio_formateado", "is_active")
    list_filter = ("brand", "year", "transmission", "color", "is_active")
    search_fields = ("brand", "model")
    readonly_fields = ("preview",)
    fieldsets = (
        (None, {
            "fields": (("brand", "model"), ("year", "transmission"), ("color", "mileage_km"), "price_cop", "is_active")
        }),
        ("Imagen", {
            "fields": ("image", "preview"),
        }),
        ("Metadatos", {
            "fields": ("created_at",),
        }),
    )
    readonly_fields = ("created_at", "preview")

    def precio_formateado(self, obj):
        # Separador de miles estilo colombiano
        return f"${obj.price_cop:,.0f}".replace(",", ".")
    precio_formateado.short_description = "Precio (COP)"

    def preview(self, obj):
        if not obj.image:
            return "—"
        return f'<img src="{obj.image.url}" style="max-width:280px; height:auto; border-radius:8px;" />'
    preview.allow_tags = True
