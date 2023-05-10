from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    path('buyer_registration/', views.buyer_registration, name='buyer_registration'),
    path('Buyer_login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='B_login'),

    path('dashboard/', views.dashboard, name='dashboard'),
]