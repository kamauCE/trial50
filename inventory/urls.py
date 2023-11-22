from django.urls import path

import inventory.views
from .views import add_product, product_detail, all_products, search_product_by_barcode, delete_product, edit_product, \
  search_and_add_to_cart, cart_view, handlelogin, handlelogout, signup, checkout_view, add_to_cart,home

urlpatterns = [
  path('add/', add_product, name='add_product'),
  path('product/<str:barcode>/', product_detail, name='product_detail'),
  path('all/', all_products, name='all_products'),
  path('search/', search_product_by_barcode, name='search_product_by_barcode'),
  path('delete/<str:barcode>/', delete_product, name='delete_product'),
  path('edit/<str:barcode>/', edit_product, name='edit_product'),
  path('search_and_add_to_cart/<str:barcode>/', search_and_add_to_cart, name='search_and_add_to_cart'),
  path('cart/', cart_view, name='cart_view'),
  path('login', inventory.views.handlelogin, name='handlelogin'),
  path('logout', inventory.views.handlelogout, name='handlelogout'),
  path('signup', signup, name='signup'),
  path('checkout/', checkout_view, name='checkout'),
  path('add_to_cart/<str:barcode>/', add_to_cart, name='add_to_cart'),
  path('',home, name='home'),


]
