from django.http import Http404,HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify

from .models import Vendor
from apps.product.models import *
from .forms import ProductForm

from datetime import datetime
import csv

# Create your views here.
def vendor_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('login')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'vendors/vendor_registration.html', context)

@login_required
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()
    total_orders = vendor.orders.all().count()
    total_products = vendor.products.all().count()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.Vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    context = {'vendor':vendor, 'products':products, 'total_products':total_products, 'orders':orders, 'total_orders':total_orders}
    return render(request, 'vendors/vendor_admin.html', context)

def orders(request):
    vendor = request.user.vendor
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.Vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    context = {'orders':orders}
    return render(request, 'vendors/orders.html', context)

def paid_orders(request,pk):
    vendor = request.user.vendor
    paid_order = vendor.orders.filter(fully_paid=True, id=pk).first()

    if not paid_order:
        # If the paid order doesn't exist, return a 404 error
        raise Http404("Paid order does not exist")

    context = {'paid_order': paid_order,}
    return render(request, 'vendors/paid_orders.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()

    context = {'form':form}
    return render(request, 'vendors/add_product.html', context)

def edit_product(request,pk):
    vendor = request.user.vendor
    product = vendor.products.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm(instance=product)

    context = {'form':form, 'product':product}
    return render(request, 'vendors/edit_product.html', context)

def all_products(request):
    vendor = request.user.vendor
    all_products = vendor.products.all()

    context = {'vendor':vendor, 'all_products':all_products}
    return render(request, 'vendors/all_products.html', context)


@login_required
def edit_vendor(request):
    vendor = request.user.vendor

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            vendor.created_by.email = email
            vendor.created_by.save()

            vendor.name = name
            vendor.save()

            return redirect('vendor_admin')
    
    return render(request, 'vendors/edit_vendor.html', {'vendor': vendor})

def export_csv(request):
    current_date_time = datetime.now()
    response = HttpResponse(
        content_type = 'text/csv',
        headers = {'Content-Disposition': f'attachment; filename="order_records {str(current_date_time)}.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['first_name','Last Name','Email','Residence','Phone'])

    vendor = request.user.vendor
    orders = vendor.orders.all()

    for order in orders:
        writer.writerow([order.first_name, order.last_name, order.email, order.phone, order.address])

    return response 