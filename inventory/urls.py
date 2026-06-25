from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("hod/", hod_dashboard, name="hod_dashboard"),
    path("labtech/", labtech_dashboard, name="labtech_dashboard"),
]