# models.py
from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):

    NAME_CHOICES = [
      ('Concealer','Concealer'),
      ('Mascara','Mascara'),
      ('Blush','Blush'),
      ('Foundation','Foundation'),
      ('Eye shadow','Eye shadow'),
      ('Eye liner','Eye liner'),
      ('Primer','Primer'),
      ('Clinique','Clinique'),
      ('Bronzer','Bronzer'),
      ('Highlighter','Highlighter'),
      ('Maybelline','Maybelline'),
      ('Powder','Powder'),
      ('Mosturizer','Mosturizer'),
      ('Cream','Cream'),
      ('Shampoo','Shampoo'),
    ]

    name = models.CharField(max_length=255, choices=NAME_CHOICES)
    barcode = models.CharField(max_length=14, unique=True)
    quantity_available = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)




    def __str__(self):
      return self.name


class Cart(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  products = models.ManyToManyField(Product, through='CartItem')


class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=0)

