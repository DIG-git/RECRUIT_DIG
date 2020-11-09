from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)


class EmployeeInfo(models.Model):
    GenderChoice = (
        ("M", "Male"), ("F", "Female")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    Gender = models.CharField(max_length=6, choices=GenderChoice)
    Email = models.EmailField(max_length=100, blank=True, null=True)
    Address = models.CharField(max_length=50, blank=True, null=True)
    Phone = models.CharField(max_length=12, blank=True, null=True)


class CompanyInfo(models.Model):
    CategoryChoice = (
        ("G", "Government"),
        ("IT", "IT & Telecommunication"),
        ("H", "Hospitality"),
        ("AM", "Administration/Management"),
        ("NI", "NGO/INGO"),
        ("T", "Teaching/Education"),
        ("Ar", "Architecture/Interior Design"),
        ("S", "Sales/Public Relation")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    Category = models.CharField(max_length=6, choices=CategoryChoice)
    Email = models.EmailField(max_length=100, blank=True, null=True)
    Address = models.CharField(max_length=50, blank=True, null=True)
    Phone = models.CharField(max_length=12, blank=True, null=True)

