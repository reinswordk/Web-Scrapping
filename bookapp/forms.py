from django import forms
from .models import BookSearch, MyScrape
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import MyModel, Book

class BookSearchForm(forms.ModelForm):
    name_of_book = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': "form-control me-2", 'placeholder': 'Enter name of book'
    }))
    class Meta:
        model = BookSearch
        fields = ['name_of_book',]

class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length = 100, widget = forms.TextInput(attrs={
        'class' : 'form-control', 'placeholder': 'Enter Username'
    }))

    email = forms.CharField(max_length = 100, widget = forms.EmailInput(attrs={
        'class' : 'form-control', 'placeholder': 'Enter Email Address'
    }))

    password1 = forms.CharField(max_length = 100, widget = forms.PasswordInput(attrs={
        'class' : 'form-control', 'placeholder': 'At least eight characters'
    }))
    password2 = forms.CharField(max_length = 100, widget = forms.PasswordInput(attrs={
        'class' : 'form-control', 'placeholder': 'Confirm Password'
    }))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class MyForm(forms.ModelForm):
  class Meta:
    model = MyModel
    fields = ["fullname", "mobile_number",]
    labels = {'fullname': "Name", "mobile_number": "Mobile Number",}

class InputBuku(forms.ModelForm):
  class Meta:
    model = Book
    fields = ["title", "slug", "cover_image", "author", "summary", "publisher", "rilis", "language", "halaman", "compatible", "genre", "harga", "rating", "ratingsum", "category",]
    labels = {'title': "Judul Buku", 'slug': "Slug", 'cover_image': "URL Sampul", 'author': "Penulis", 'summary': "Ringkasan", 'publisher': "Penerbit", 'rilis': "Tanggal Terbit", 'language': "Bahasa", 'halaman': "Halaman", 'compatible': "Kompatibel untuk", 'genre': "Genre", 'harga': "Harga", 'rating': "Rating", 'ratingsum': "Jumlah Review", 'category': "Category",}

class Scrape(forms.ModelForm):
  class Meta:
    model = MyScrape
    fields = ["link",]
    labels = {'link': "URL Scrape",}