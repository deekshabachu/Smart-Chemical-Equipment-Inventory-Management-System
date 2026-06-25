from django.shortcuts import render
from .models import Chemical, Equipment, Alert, Lab

def home(request):
    return render(request, "inventory/home.html")

def hod_dashboard(request):

    context = {
        "chemical_count": Chemical.objects.count(),
        "equipment_count": Equipment.objects.count(),
        "alert_count": Alert.objects.count(),
        "lab_count": Lab.objects.count(),
    }

    return render(request, "inventory/dashboard_hod.html", context)


def labtech_dashboard(request):

    user_lab = request.user.userprofile.lab

    context = {
        "chemical_count": Chemical.objects.filter(lab=user_lab).count(),
        "equipment_count": Equipment.objects.filter(lab=user_lab).count(),
        "alert_count": Alert.objects.filter(lab=user_lab).count(),
    }

    return render(request, "inventory/dashboard_labtech.html", context)