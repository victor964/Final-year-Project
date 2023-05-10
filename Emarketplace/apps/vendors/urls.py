from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('vendor_registration/', views.vendor_registration, name='vendor_registration'),
    path('vendor_admin/', views.vendor_admin, name='vendor_admin'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('all-products/', views.all_products, name='all_products'),
    path('edit-vendor/', views.edit_vendor, name='edit_vendor'),
    path('orders/', views.orders, name='orders'),

    path('paid-orders/<int:pk>/', views.paid_orders, name='paid_orders'),

    path('exportcsv/', views.export_csv, name='export_csv'),

    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('login/', auth_views.LoginView.as_view(template_name='vendors/login.html'), name='login'),

]