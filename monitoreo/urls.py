"""
URL configuration for monitoreo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth (HU6-HU8) :contentReference[oaicite:8]{index=8}
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', core_views.register, name='register'),

    # Password reset (simulado por consola en U1) :contentReference[oaicite:9]{index=9}
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Core
    path('', core_views.dashboard, name='dashboard'),                 # HU1 + HU5 :contentReference[oaicite:10]{index=10}
    path('devices/', core_views.devices_list, name='devices_list'),   # HU2 :contentReference[oaicite:11]{index=11}
    path('devices/<int:pk>/', core_views.device_detail, name='device_detail'),  # HU3 :contentReference[oaicite:12]{index=12}
    path('measurements/', core_views.measurements_list, name='measurements_list'),  # HU4 :contentReference[oaicite:13]{index=13}
]

