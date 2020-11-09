from django.contrib import admin
from .models import EmployeeInfo, CompanyInfo, User

# Register your models here.
admin.site.register(EmployeeInfo)
admin.site.register(CompanyInfo)
admin.site.register(User)
