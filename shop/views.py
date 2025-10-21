
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from .models import Car
from .forms import CarForm
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import models
from django.conf import settings
import os
from decimal import Decimal


def home(request):
    """Vista de la página de inicio.

    Parámetros:
    - request: HttpRequest

    Retorna:
    - render de `shop/home.html` con contexto vacío (puedes añadir datos aquí si los necesitas).
    """
    # construir lista de imágenes para el carrusel desde MEDIA_ROOT/Home
    carousel_images = []
    try:
        media_home_dir = os.path.join(settings.MEDIA_ROOT, 'Home')
        if os.path.isdir(media_home_dir):
            for fname in sorted(os.listdir(media_home_dir)):
                if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    # usar MEDIA_URL para construir la URL pública
                    url = settings.MEDIA_URL.rstrip('/') + '/Home/' + fname
                    carousel_images.append(url)
    except Exception:
        carousel_images = []

    # seleccionar un coche destacado cualquiera (el más reciente activo)
    featured_car = Car.objects.filter(is_active=True).order_by('-created_at').first()
    featured_list = [featured_car] if featured_car else []

    context = {
        'carousel_images': carousel_images,
        'featured_car': featured_car,
        'featured_list': featured_list,
    }
    return render(request, 'shop/home.html', context)

def catalogo(request):
    """Listado público (catálogo) de coches.

    Este view aplica los filtros contenidos en `CarFilterForm` (marca, color,
    año mínimo/máximo, precio mínimo/máximo) y devuelve una página con
    paginación (12 elementos por página).

    Parámetros:
    - request: HttpRequest; puede incluir parámetros GET para filtrar:
      - brand, color, year_min, year_max, price_min, price_max

    Retorna:
    - render de `shop/catalogo.html` con 'page' (paginator page) y 'filter_form'.
    """
    from .forms import CarFilterForm

    qs = Car.objects.filter(is_active=True).order_by('-created_at')

    # aplicar filtros desde el formulario
    form = CarFilterForm(request.GET or None)
    if form.is_valid():
        brand = form.cleaned_data.get('brand')
        color = form.cleaned_data.get('color')
        year_min = form.cleaned_data.get('year_min')
        year_max = form.cleaned_data.get('year_max')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')

        if brand:
            qs = qs.filter(brand__icontains=brand)
        if color:
            qs = qs.filter(color__icontains=color)
        if year_min:
            qs = qs.filter(year__gte=year_min)
        if year_max:
            qs = qs.filter(year__lte=year_max)
        if price_min:
            qs = qs.filter(price_cop__gte=price_min)
        if price_max:
            qs = qs.filter(price_cop__lte=price_max)

    page = Paginator(qs, 12).get_page(request.GET.get('page'))
    context={'page': page, 'filter_form': form}
    return render(request, 'shop/catalogo.html', context)

def contacto(request):
    context={}
    return render(request, 'shop/contacto.html', context)

def cart(request):
    context={}
    return render(request, 'shop/cart.html', context)

def checkout(request):
    context={}
    return render(request, 'shop/checkout.html', context)


def car_detail(request, pk):
    """Ficha detallada de un coche.

    Parámetros:
    - pk: id del coche

    Retorna el template `shop/car_detail.html` con el objeto `car`.
    """
    car = get_object_or_404(Car, pk=pk, is_active=True)
    return render(request, 'shop/car_detail.html', {'car': car})


def search_suggestions(request):
    """Endpoint AJAX que devuelve sugerencias en formato JSON.

    Responde a peticiones GET con parámetro `q` y devuelve una lista JSON de
    hasta 10 coincidencias. Cada elemento incluye campos útiles para pintar
    mini-tarjetas en el frontend: label, pk, image, year, mileage_km, price.

    Esto se usa para autocompletar y para mostrar resultados inmediatos
    debajo del input de búsqueda.
    """
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        qs = Car.objects.filter(is_active=True).filter(
            models.Q(brand__icontains=q) | models.Q(model__icontains=q)
        ).order_by('-created_at')[:10]
        for c in qs:
            # formateo sencillo del precio para mostrar (miles con puntos)
            price = getattr(c, 'price_cop', None)
            price_text = ''
            if price is not None:
                try:
                    if isinstance(price, Decimal) and price % 1 == 0:
                        # precio entero, sin decimales
                        price_text = f"{int(price):,}".replace(',', '.')
                    else:
                        # dos decimales, miles con punto y coma decimal
                        price_text = f"{price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                except Exception:
                    price_text = str(price)

            # construir URL de imagen con prefijo de MEDIA_URL si fuera necesario
            image_url = ''
            if hasattr(c, 'image') and c.image:
                try:
                    image_url = c.image.url
                    if not str(image_url).startswith(str(settings.MEDIA_URL)):
                        image_url = str(settings.MEDIA_URL).rstrip('/') + '/' + str(c.image.name).lstrip('/')
                except Exception:
                    image_url = str(settings.MEDIA_URL).rstrip('/') + '/' + str(c.image.name).lstrip('/')

            results.append({
                'label': f"{c.brand} {c.model} ({c.year})",
                'pk': c.pk,
                'image': image_url,
                'year': c.year,
                'mileage_km': c.mileage_km,
                'price': price_text,
            })
    return JsonResponse(results, safe=False)


def search_results(request):
    """Devuelve HTML renderizado con tarjetas de coches que coinciden (para AJAX).

    Se utiliza desde el frontend para reemplazar la rejilla principal con
    resultados filtrados sin recargar la página.
    """ 
    q = request.GET.get('q', '').strip()
    qs = Car.objects.filter(is_active=True).order_by('-created_at')
    if q:
        qs = qs.filter(models.Q(brand__icontains=q) | models.Q(model__icontains=q) | models.Q(color__icontains=q))
    
    qs = qs[:50]
    return render(request, 'shop/_car_cards.html', {'cars': qs})

def administrador(request):
    # si el usuario es staff mostramos un panel con opciones de administración
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'shop/admin_dashboard.html', {})
    # para usuarios no staff mostramos la página de administrador actual (informativa)
    context={}
    return render(request, 'shop/administrador.html', context)
def staff_required(view):
    return login_required(user_passes_test(lambda u: u.is_staff, login_url="login")(view))

