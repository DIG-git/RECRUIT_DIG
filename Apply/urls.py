from django.urls import path
from . import views

urlpatterns = [
    path('apply/<str:job_id>/', views.apply, name='apply'),
    path('add_apply/<str:job_id>/', views.add_apply, name='add_apply'),
    path('add_jobs', views.add_jobs, name='add_jobs'),
    path('post_jobs', views.post_jobs, name='post_jobs'),
    path('aptitude_form/<int:job_id>/', views.aptitude_form, name='aptitude_form'),
    path('aptitude_result/<int:job_id>/', views.aptitude_result, name='aptitude_result'),
]