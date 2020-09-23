from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('jobs', views.jobs, name='jobs'),
    path('job_category', views.category, name='job_category'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('job_detail/<str:pk>/', views.job_detail, name='job_detail'),
]