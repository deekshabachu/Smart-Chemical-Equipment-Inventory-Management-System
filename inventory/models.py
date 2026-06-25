from django.db import models
from django.contrib.auth.models import User
# Create your models here.



#Lab
class Lab(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


#Chemical
class Chemical(models.Model):
    HAZARD_LEVEL_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    min_threshold = models.IntegerField()
    max_threshold = models.IntegerField()
    expiry_date = models.DateField()
    hazard_level = models.CharField(max_length=10, choices=HAZARD_LEVEL_CHOICES)
    msds_link = models.URLField()
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.lab.name})"


#Equipment
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    available_quantity = models.IntegerField()
    min_threshold = models.IntegerField()
    max_threshold = models.IntegerField()
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.lab.name})"


#LabSettings
class LabSettings(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    student_intake = models.IntegerField()
    scaling_factor = models.FloatField(default=1.0)
    scaling_applied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lab.name} Settings"



#Alert
class Alert(models.Model):
    ALERT_TYPE_CHOICES = [
        ("CHEMICAL", "Chemical"),
        ("EQUIPMENT", "Equipment"),
    ]

    message = models.TextField()
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPE_CHOICES)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alert_type} Alert ({self.lab.name})"

class UserProfile(models.Model):
    

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lab = models.ForeignKey(
        Lab,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username