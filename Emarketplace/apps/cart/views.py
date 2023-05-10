import stripe
from django.shortcuts import render,redirect
from .cart import Cart

# from django_daraja.mpesa.core import MpesaClient
from django.conf import settings
from django.contrib import messages
from .forms import CheckoutForm
from apps.order.utilities import checkout, notify_customer, notify_vendor

# Create your views here.
def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
         form = CheckoutForm(request.POST)

         if form.is_valid():
              stripe.api_key = settings.STRIPE_SECRET_KEY

              stripe_token = form.cleaned_data['stripe_token']

              try:
                charge = stripe.Charge.create(
                    amount = int(cart.get_total_cost() * 100),
                    currency = 'USD',
                    description = 'Charge from VBizz',
                    source = stripe_token
                )

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                place = form.cleaned_data['place']

                order = checkout(request, first_name, last_name, email, phone, address, place, cart.get_total_cost())

                cart.clear()

                notify_customer(order)
                notify_vendor(order)

                return redirect('success')
              except Exception:
                messages.error(request,'There was something wrong with the payment')

    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    context = {'form':form, 'stripe_pub_key':settings.STRIPE_PUB_KEY}
    return render(request, 'cart/cart.html', context)

def success(request):

    context = {}
    return render(request, 'cart/success.html', context)
