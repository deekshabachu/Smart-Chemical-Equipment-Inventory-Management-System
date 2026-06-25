from django.contrib import admin
from .models import Lab, Chemical, Equipment, LabSettings, Alert, UserProfile
from .utils import apply_scaling_for_lab, create_chemical_alert, create_equipment_alert


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    pass


@admin.register(Chemical)
class ChemicalAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "min_threshold", "max_threshold", "lab")
    list_editable = ("min_threshold",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        create_chemical_alert(obj)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "available_quantity", "min_threshold", "max_threshold", "lab")
    list_editable = ("min_threshold",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        create_equipment_alert(obj)


@admin.register(LabSettings)
class LabSettingsAdmin(admin.ModelAdmin):
    list_display = ("lab", "student_intake", "scaling_factor", "scaling_applied")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        apply_scaling_for_lab(obj)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("alert_type", "message", "lab", "created_at")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "lab")