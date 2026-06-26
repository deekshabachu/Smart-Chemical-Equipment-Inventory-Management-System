from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from .models import Chemical, Equipment, Alert, Lab
from .models import UserProfile

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

def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.groups.filter(name="HOD").exists():

                return redirect("hod_dashboard")

            elif user.groups.filter(name="Lab Technician").exists():

                return redirect("labtech_dashboard")

            else:

                return redirect("home")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "inventory/login.html"
    )


def logout_view(request):

    logout(request)

    return redirect("home")

def chemicals(request):

    if request.user.groups.filter(name="HOD").exists():
        chemicals = Chemical.objects.all()
    else:
        user_lab = request.user.userprofile.lab
        chemicals = Chemical.objects.filter(lab=user_lab)

    # Search
    search = request.GET.get("search")

    if search:
        chemicals = chemicals.filter(name__icontains=search)

    # Hazard Filter
    hazard = request.GET.get("hazard")

    if hazard:
        chemicals = chemicals.filter(hazard_level=hazard)

    context = {
        "chemicals": chemicals,
        "search": search,
        "hazard": hazard,
    }

    return render(request, "inventory/chemicals.html", context)