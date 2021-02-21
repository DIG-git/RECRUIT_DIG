from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('Employee', views.dashboard1, name='dashboard1'),
    path('UpdateApplication/<str:applicant_id>', views.update_apply_form, name='update_apply_form'),
    path('ApplicationUpdate/<str:employee_id>', views.update_employee, name='update_employee'),
    path('DeleteApplication/<str:applicant_id>', views.delete_employee, name='delete_application'),
    path('Applicants/<str:job_id>/', views.applicants, name='applicants'),
    path('UpdateJob/<str:job_id>', views.update_job_form, name='update_job_form'),
    path('JobUpdate/<str:job_id>', views.update_job, name='update_job'),
    path('DeleteJob/<str:job_id>', views.delete_job, name='delete_job'),
    path('Compatible', views.description_list, name='compatible'),
]