
from django import forms
from .models import Car
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal, InvalidOperation

class CarForm(forms.ModelForm):
    """Formulario para crear/editar `Car`.

    - `price_cop` se gestiona como `CharField` para aceptar formatos locales
      (por ejemplo: "1.234.567,89") y se normaliza en `clean_price_cop`.
    """

    # Acepta entrada de texto con separadores de miles y la normaliza en clean_price_cop
    price_cop = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "input", "inputmode": "decimal", "placeholder": "1.234.567,89"}))

    class Meta:
        model = Car
        fields = ["brand", "model", "year", "transmission", "body_type", "color", "mileage_km", "price_cop", "image", "is_active"]
        widgets = {
            "brand": forms.TextInput(attrs={"class": "input"}),
            "model": forms.TextInput(attrs={"class": "input"}),
            "year": forms.NumberInput(attrs={"class": "input"}),
            "transmission": forms.Select(attrs={"class": "select"}),
            "body_type": forms.Select(attrs={"class": "select"}),
            "color": forms.TextInput(attrs={"class": "input"}),
            "mileage_km": forms.NumberInput(attrs={"class": "input"}),
            # El widget de price_cop está definido en el campo anterior
            "image": forms.ClearableFileInput(attrs={"class": "input"}),
            "is_active": forms.CheckboxInput(),
        }

    def clean_price_cop(self):
        """Normaliza cadenas numéricas y devuelve Decimal.

        Soporta formatos como '1.234.567,89' (miles con punto, coma decimal)
        o '1234567.89' (punto decimal). Si la conversión falla lanza ValidationError.
        """
        raw = self.cleaned_data.get("price_cop")
        if raw in (None, ""):
            return raw
        # Si ya es Decimal (poco probable porque el widget es TextInput), devolver tal cual
        if isinstance(raw, Decimal):
            return raw
        s = str(raw).strip()
        # eliminar espacios
        s = s.replace(" ", "")
        # Si hay una única coma y posiblemente puntos como separadores de miles
        if "," in s and s.count(",") == 1:
            # eliminar puntos usados como separador de miles
            s = s.replace(".", "")
            # reemplazar la coma decimal por punto
            s = s.replace(",", ".")
        else:
            # eliminar puntos (miles) y convertir comas restantes a punto
            s = s.replace(".", "")
            s = s.replace(",", ".")
        try:
            return Decimal(s)
        except InvalidOperation:
            raise forms.ValidationError("Introduce un precio válido, por ejemplo: 1.234.567,89 o 1234567.89")


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput(), help_text="Dejar vacío para no cambiar la contraseña")

    class Meta:
        model = User
        fields = ["username", "email", "is_staff", "is_active", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get("password")
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user


class CarFilterForm(forms.Form):
    """Formulario sencillo para filtrar el catálogo por marca, color, año y rango de precio.

    Los campos de precio se introducen como texto para aceptar separadores locales
    y se parsean en `_parse_price`.
    """
    brand = forms.CharField(label="Marca", required=False, widget=forms.TextInput(attrs={"class": "input", "placeholder": "Marca"}))
    color = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "input", "placeholder": "Color"}))
    year_min = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"class": "input", "placeholder": "Año desde"}))
    year_max = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"class": "input", "placeholder": "Año hasta"}))
    price_min = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "input", "placeholder": "Precio min (ej. 1.000.000)"}))
    price_max = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "input", "placeholder": "Precio max (ej. 5.000.000)"}))

    def clean_price_min(self):
        v = self.cleaned_data.get('price_min')
        if not v:
            return None
        return self._parse_price(v)

    def clean_price_max(self):
        v = self.cleaned_data.get('price_max')
        if not v:
            return None
        return self._parse_price(v)

    def _parse_price(self, raw):
        s = str(raw).strip().replace(' ', '').replace('.', '').replace(',', '.')
        try:
            return Decimal(s)
        except Exception:
            raise forms.ValidationError('Introduce un precio válido')
