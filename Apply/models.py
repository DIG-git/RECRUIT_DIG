from django.db import models
from authentication.models import User


class Job(models.Model):
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
    userID = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    comp_name = models.CharField(max_length=30, blank=True, null=True)
    job_category = models.CharField(max_length=6, choices=CategoryChoice)


class EmployeeApplicants(models.Model):
    userID = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, default=None)
    jobID = models.ForeignKey(Job, null=True, on_delete=models.CASCADE, default=None)
    fname = models.CharField(max_length=25)
    mname = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    contact = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=25)
    email = models.EmailField(max_length=25, blank=True, null=True)
    gender = models.CharField(max_length=10)
    dob = models.DateTimeField()
    resume = models.FileField(upload_to="resume/")


class JobRequirements(models.Model):
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, default=None)
    post = models.CharField(max_length=30, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)
    openings = models.IntegerField(blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    hours = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=10)
    fromdate = models.DateTimeField()
    todate = models.DateTimeField()
    description = models.FileField(upload_to="description/")
