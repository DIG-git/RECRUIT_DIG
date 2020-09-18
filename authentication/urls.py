from django.urls import path
from . import views

urlpatterns = [
                  path('register', views.register, name='register'),
                  path('login', views.login, name="login"),
                  path('logout', views.logout, name='logout'),
                  path('register_company', views.register_Company, name="register_company"),
                  path('login_company', views.login_Company, name="login_company")
              ]
