from django.shortcuts import render,redirect
from apps.product.models import Product

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Buyer

from apps.vendors.views import vendor_registration

# Create your views here.
def home(request):
    
    context = {}
    return render(request, 'base/home.html', context)

def buyer_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            buyer = Buyer.objects.create(name=user.username, created_by=user)

            return redirect('B_login')
    else:
        form = UserCreationForm()
    
    context = {'form':form}
    return render(request, 'base/buyer_registration.html', context)

def dashboard(request):
    newest_products = Product.objects.all()[0:8]
    featured_products = Product.objects.all()[:3]
    
    context = {'newest_products':newest_products,'featured_products':featured_products}
    return render(request, 'base/dashboard.html', context)
