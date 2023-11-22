# forms.py
from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = '__all__'

  NAME_CHOICES = [
    ('Concealer', 'Concealer'),
    ('Mascara', 'Mascara'),
    ('Blush', 'Blush'),
    ('Foundation', 'Foundation'),
    ('Eye shadow', 'Eye shadow'),
    ('Eye liner', 'Eye liner'),
    ('Primer', 'Primer'),
    ('Clinique', 'Clinique'),
    ('Bronzer', 'Bronzer'),
    ('Highlighter', 'Highlighter'),
    ('Maybelline', 'Maybelline'),
    ('Powder', 'Powder'),
    ('Mosturizer', 'Mosturizer'),
    ('Cream', 'Cream'),
    ('Shampoo', 'Shampoo'),
  ]

  name = forms.ChoiceField(choices=NAME_CHOICES)

  def __init__(self, *args, **kwargs):
    super(ProductForm, self).__init__(*args, **kwargs)


class BarcodeSearchForm(forms.Form):
  barcode = forms.CharField(max_length=14)
  quantity = forms.IntegerField(label='Quantity', min_value=1)



class CustomSignUpForm(UserCreationForm):
    class Meta:
      model = User
      fields = ['username', 'password1', 'password2']

      widgets = {
        'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
        # 'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        # 'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
      }
