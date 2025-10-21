from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from .models import Car
from django.db import models
from .forms import CarForm
from django.contrib.auth.models import User
from .forms import UserForm
from django.http import HttpResponse
from django.template.loader import render_to_string

def staff_required(view):
    """Decorador compacto para exigir que el usuario sea staff.

    Envuelve `login_required` y `user_passes_test` para permitir solo
    accesos de personal administrativo.
    """
    return login_required(user_passes_test(lambda u: u.is_staff)(view))

@staff_required
def admin_cars(request):
    from .forms import CarFilterForm

    qs = Car.objects.all().order_by("-created_at")

    # formulario para filtros de parámetros (marca, color, año, precio)
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

    # búsqueda de texto libre 'q' (marca/modelo/color) - se comporta como en el catálogo
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(models.Q(brand__icontains=q) | models.Q(model__icontains=q) | models.Q(color__icontains=q))

    page = Paginator(qs, 10).get_page(request.GET.get("page"))

    # Si es llamada AJAX, devolver solo el partial con las filas de la tabla
    if request.GET.get('ajax') == '1':
        html = render_to_string('shop/_admin_car_rows.html', {'page': page}, request=request)
        return HttpResponse(html)

    return render(request, "shop/administrador.html", {"page": page, "filter_form": form})

@staff_required
def admin_car_create(request):
    """Crear un nuevo carro desde el panel administrativo."""
    form = CarForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Carro creado.")
        return redirect("admin_cars")
    return render(request, "shop/admin_car_form.html", {"form": form, "title": "Nuevo carro"})

@staff_required
def admin_car_edit(request, pk):
    """Editar un carro existente (staff)."""
    car = get_object_or_404(Car, pk=pk)
    form = CarForm(request.POST or None, request.FILES or None, instance=car)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Carro actualizado.")
        return redirect("admin_cars")
    return render(request, "shop/admin_car_form.html", {"form": form, "title": f"Editar: {car}"})

@staff_required
def admin_car_delete(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        car.delete()
        messages.success(request, "Carro eliminado.")
        return redirect("admin_cars")
    return render(request, "shop/admin_car_delete.html", {"car": car})


@staff_required
def admin_users(request):
    """Listado de usuarios para administración (solo staff)."""
    qs = User.objects.all().order_by("username")
    page = Paginator(qs, 20).get_page(request.GET.get("page"))
    return render(request, "shop/admin_users.html", {"page": page})


@staff_required
def admin_user_create(request):
    form = UserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Usuario creado.")
        return redirect("admin_users")
    return render(request, "shop/admin_user_form.html", {"form": form, "title": "Nuevo usuario"})


@staff_required
def admin_user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Usuario actualizado.")
        return redirect("admin_users")
    return render(request, "shop/admin_user_form.html", {"form": form, "title": f"Editar: {user.username}"})


@staff_required
def admin_user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, "Usuario eliminado.")
        return redirect("admin_users")
    return render(request, "shop/admin_user_delete.html", {"user": user})
