# Create your views here.
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib.auth import login
from .models import Category, Zone, Device, Measurement, Alert, Organization, UserProfile
from .forms import SignUpForm


@login_required
def dashboard(request):
    org = request.user.userprofile.organization
    # últimas 10 mediciones (fecha/hora, dispositivo, valor)
    last_measurements = (
        Measurement.objects
        .filter(organization=org, deleted_at__isnull=True)
        .select_related('device')
        .order_by('-created_at')[:10]
    )
    # dispositivos por categoría y por zona (conteos)
    devices_by_category = (
        Device.objects.filter(organization=org, deleted_at__isnull=True)
        .values('category__name').annotate(total=Count('id')).order_by('category__name')
    )
    devices_by_zone = (
        Device.objects.filter(organization=org, deleted_at__isnull=True)
        .values('zone__name').annotate(total=Count('id')).order_by('zone__name')
    )
    # alertas de la semana por severidad
    start_week = timezone.now() - timedelta(days=7)
    alerts_week = (
        Alert.objects.filter(organization=org, deleted_at__isnull=True, created_at__gte=start_week)
        .values('severity').annotate(total=Count('id')).order_by('severity')
    )
    recent_alerts = (
        Alert.objects.filter(organization=org, deleted_at__isnull=True)
        .select_related('device').order_by('-created_at')[:5]
    )
    return render(request, 'core/dashboard.html', {
        'last_measurements': last_measurements,
        'devices_by_category': devices_by_category,
        'devices_by_zone': devices_by_zone,
        'alerts_week': alerts_week,
        'recent_alerts': recent_alerts,
    })


@login_required
def devices_list(request):
    org = request.user.userprofile.organization
    category_id = request.GET.get('category')
    qs = Device.objects.filter(organization=org, deleted_at__isnull=True).select_related('category', 'zone')
    if category_id:
        qs = qs.filter(category_id=category_id)
    categories = Category.objects.filter(organization=org, deleted_at__isnull=True)
    return render(request, 'core/devices_list.html', {
        'devices': qs.order_by('name'),
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })


@login_required
def device_detail(request, pk):
    org = request.user.userprofile.organization
    device = get_object_or_404(Device, pk=pk, organization=org, deleted_at__isnull=True)
    measurements = Measurement.objects.filter(device=device, deleted_at__isnull=True).order_by('-created_at')
    alerts = Alert.objects.filter(device=device, deleted_at__isnull=True).order_by('-created_at')
    return render(request, 'core/device_detail.html', {
        'device': device,
        'measurements': measurements,
        'alerts': alerts,
    })


@login_required
def measurements_list(request):
    org = request.user.userprofile.organization
    measurements = (
        Measurement.objects.filter(organization=org, deleted_at__isnull=True)
        .select_related('device').order_by('-created_at')[:50]  # simple cap de 50
    )
    return render(request, 'core/measurements_list.html', {'measurements': measurements})


def register(request):
    # HU7 — Registro de empresa: /register/ con nombre empresa, correo, contraseña. :contentReference[oaicite:7]{index=7}
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            org = Organization.objects.create(
                name=form.cleaned_data['organization_name'],
                email=form.cleaned_data['email']
            )
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            UserProfile.objects.create(user=user, organization=org)
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})
