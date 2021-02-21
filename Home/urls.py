from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('jobs', views.jobs, name='jobs'),
    path('job_list', views.category, name='job_list'),
    path('job_category/<str:id>/', views.job_category, name='job_category'),
    path('job_detail/<str:pk>/', views.job_detail, name='job_detail'),
    path('personality_test', views.personality_test, name='personality_test'),
    path('personality_score', views.personality_score, name='personality_score'),
    path('search_result', views.search, name='search'),
    path('about', views.about, name='about'),
]