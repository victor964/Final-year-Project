from django.conf import settings
import smtplib
from django.template.loader import render_to_string
from apps.cart.cart import Cart
from .models import *

def checkout(request, first_name, last_name, email, address, place, phone, amount):
    order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, address=address, place=place, phone=phone, paid_amount=amount)

    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], Vendor=item['product'].vendor, price=item['product'].price, quantity=item['quantity'])
    
        order.vendors.add(item['product'].vendor)

    return order

def notify_vendor(order):
    for vendor in order.vendors.all():
        with smtplib.SMTP("smtp.office365.com",587) as connection:
            connection.starttls()
            connection.login(user=settings.MY_EMAIL, password=settings.PASSWORD)
            connection.sendmail(
                from_addr=settings.MY_EMAIL,
                to_addrs=vendor.created_by.email,
                msg=render_to_string('order/email_notify_vendor.html', {'order': order, 'vendor': vendor})
            )

def notify_customer(order):
    with smtplib.SMTP("smtp.office365.com",587) as connection:
        connection.starttls()
        connection.login(user=settings.MY_EMAIL, password=settings.PASSWORD)
        connection.sendmail(
            from_addr=settings.MY_EMAIL,
            to_addrs=order.email,
            msg=render_to_string('order/email_notify_buyer.html', {'order': order})
        )