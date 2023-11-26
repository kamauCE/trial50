# views.py
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .forms import BarcodeSearchForm
from .forms import CustomSignUpForm
from .models import Product, Cart, CartItem
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect


def add_product(request):
  if request.method == 'POST':
    form = ProductForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      barcode = form.cleaned_data['barcode']
      quantity = form.cleaned_data['quantity_available']
      date_added = form.cleaned_data.get('date_added')

      existing_product = Product.objects.filter(barcode=barcode).first()

      if existing_product:
        return render(request, 'product_exists.html', {'product': existing_product})

      new_product = Product(name=name, barcode=barcode, quantity_available=quantity, date_added=date_added)
      new_product.save()

      # return redirect('all_products', barcode=barcode)
      return redirect(reverse('all_products'), barcode=barcode)
  else:
    form = ProductForm()

  return render(request, 'add_product.html', {'form': form})


def all_products(request):
  products = Product.objects.all()

  if 'download_html' in request.GET:
    # If the user requested to download the HTML
    html_content = render_to_string('downloadable_products.html', {'products': products})
    response = HttpResponse(html_content, content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="products_details.html"'
    return response

  return render(request, 'all_products.html', {'products': products})



def product_detail(request, barcode):
  product = get_object_or_404(Product, barcode=barcode)

  if request.method == 'POST':
    form = ProductForm(request.POST)
    if form.is_valid():
      product.name = form.cleaned_data['name']
      product.quantity_available = form.cleaned_data['quantity_available']
      product.date_added = form.cleaned_data['date_added']  # Update other fields as needed
      product.save()
      return redirect('product_detail', barcode=product.barcode)
  else:
    form = ProductForm(
      initial={'name': product.name, 'barcode': product.barcode, 'date_added': product.date_added})
  return render(request, 'product_detail.html', {'product': product, 'form': form})


def search_product_by_barcode(request):
  products = None

  if request.method == 'POST':
    form = BarcodeSearchForm(request.POST)
    if form.is_valid():
      barcode = form.cleaned_data['barcode']
      products = Product.objects.filter(barcode=barcode)


  else:
    form = BarcodeSearchForm()

  return render(request, 'search_results.html', {'form': form, 'products': products})


def edit_product(request, barcode):
  product = get_object_or_404(Product, barcode=barcode)

  if request.method == 'POST':
    form = ProductForm(request.POST, instance=product)
    if form.is_valid():
      form.save()
      return redirect('all_products')
  else:
    form = ProductForm(instance=product)

  return render(request, 'edit_product.html', {'form': form, 'product': product})


def delete_product(request, barcode):
  product = get_object_or_404(Product, barcode=barcode)

  if request.method == 'POST':
    # Handle the confirmation of the deletion
    product.delete()
    return redirect('all_products')

  return render(request, 'confirm_delete.html', {'product': product})


@login_required
def search_and_add_to_cart(request, barcode):
  product = get_object_or_404(Product, barcode=barcode)

  if request.method == 'POST':
    form = BarcodeSearchForm(request.POST)
    if form.is_valid():
      quantity = form.cleaned_data['quantity']

      # Check if the requested quantity is available in stock
      if product.quantity_available >= quantity:
        # Add the product to the cart with the selected quantity
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()

        # Update the quantity in the database
        product.quantity_available -= quantity
        product.save()

        messages.success(request, f'{quantity} {product.name}(s) added to the cart.')
        return redirect('all_products')
      else:
        messages.error(request, 'Insufficient quantity available in stock.')
  else:
    form = BarcodeSearchForm()

  return render(request, 'search_results.html', {'form': form, 'products': [product]})


def cart_view(request):
  user = request.user
  cart = Cart.objects.get(user=user)
  cart_items = cart.cartitem_set.all()

  return render(request, 'cart_view.html', {'cart_items': cart_items})


# def handlesignup(request):
#   if request.method == 'POST':
#     username = request.POST.get("username")
#     password = request.POST.get("password")
#
#     myuser = User.objects.create_user(username, password)
#     myuser.save()
#   return render(request, 'signup.html')

def signup(request):
    if request.method == 'POST':
      form = CustomSignUpForm(request.POST)
      if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('handlelogin')  # Redirect to your desired page after successful signup
    else:
      form = CustomSignUpForm()

    return render(request, 'signup.html', {'form': form})


def handlelogin(request):
    if request.method == 'POST':
      username = request.POST.get("username")
      password = request.POST.get("password")
      myuser = authenticate(username=username, password=password)

      if myuser is not None:
        login(request, myuser)
        return redirect('all_products')
      else:
        messages.error(request, 'Incorrect login credentials')

    return render(request, 'login.html')


def handlelogout(request):
  logout(request)
  return redirect('handlelogin')


@login_required
def checkout_view(request):
  cart = Cart.objects.get(user=request.user)

  # Iterate through each cart item and delete it
  for item in cart.cartitem_set.all():
    item.delete()

  return render(request, 'checkout.html', {'cart': cart})


def add_to_cart(request, barcode):
  product = get_object_or_404(Product, barcode=barcode)

  if request.method == 'POST':
    form = ProductForm(request.POST, instance=product)
    if form.is_valid():
      cart_quantity = form.cleaned_data['cart_quantity']

      if 0 < cart_quantity <= product.quantity_available:
        # Update the quantity in the cart
        product.cart_quantity = cart_quantity
        product.save()

        # Update the quantity in the "all products" table
        product.quantity_available -= cart_quantity
        product.save()

        messages.success(request, 'Product added to cart successfully.')
        return redirect('all_products')
      else:
        messages.error(request, 'Invalid quantity selected.')
    else:
      form = ProductForm(instance=product)

    return render(request, 'add_to_cart.html', {'form': form, 'product': product})


def home(request):
  return render(request,'home.html')

def help(request):
  return render(request,'help.html')

def privacy(request):
  return render(request,'privacy.html')
