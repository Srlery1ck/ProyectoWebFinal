from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views_admin
urlpatterns = [
    path('', views.home, name='home'),
    path('carrito/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('contacto/', views.contacto, name='contacto'),
    path('administrador/', views.administrador, name='administrador'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),
    path('search_results/', views.search_results, name='search_results'),
    path("login/",  auth_views.LoginView.as_view(template_name="shop/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("administracion/", views_admin.admin_cars, name="admin_cars"),
    path("administracion/nuevo/", views_admin.admin_car_create, name="admin_car_create"),
    path("administracion/<int:pk>/editar/", views_admin.admin_car_edit, name="admin_car_edit"),
    path("administracion/<int:pk>/eliminar/", views_admin.admin_car_delete, name="admin_car_delete"),
    path("administracion/usuarios/", views_admin.admin_users, name="admin_users"),
    path("administracion/usuarios/nuevo/", views_admin.admin_user_create, name="admin_user_create"),
    path("administracion/usuarios/<int:pk>/editar/", views_admin.admin_user_edit, name="admin_user_edit"),
    path("administracion/usuarios/<int:pk>/eliminar/", views_admin.admin_user_delete, name="admin_user_delete"),
]