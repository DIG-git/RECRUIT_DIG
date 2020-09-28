from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('applicants/<str:job_id>/', views.applicants, name='applicants'),
]