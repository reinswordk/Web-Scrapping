from django.shortcuts import render, redirect
from requests.sessions import Request

import bookapp
from .models import Book, Category
from django.contrib.auth.forms import UserCreationForm
from  .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import requests
from bs4 import BeautifulSoup

from django.utils.text import slugify
import string
import random


# Create your views here.
def home(request):
    recommended_books = Book.objects.filter(recommended_books = True)
    fiction_books = Book.objects.filter(fiction_books = True)
    business_books = Book.objects.filter(business_books = True)
    return render(request, 'home.html', {'recommended_books': recommended_books,
    'business_books': business_books, 'fiction_books': fiction_books
    })

def all_books(request):
    books = Book.objects.all()
    return render(request, 'all_books.html', {'books':books})

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

def rand_slug1():
    return ''.join(str(random.randint(0, 9)) for _ in range(8))

def scrap_googlebook(url):
    global book_info
    urlnya = url
    page = requests.get(urlnya)
    soup = BeautifulSoup(page.text, 'html.parser')

    _judul = soup.select('h1[itemprop="name"] span')
    title = _judul[0].getText()

    id_semi = slugify(rand_slug1())
    id = int(id_semi)
    slug = slugify(rand_slug() + "-")

    _penulis = soup.select('a[class="hrTbp R8zArc"]')
    author = _penulis[0].getText()
    
    _desc = soup.select('span[jsslot=""]')
    summary = _desc[0].getText()

    _cover = soup.find('img', 'T75of h1kAub')
    cover_image = _cover['src']
    
    halaman = soup.find("div", string='Pages').find_next_sibling().text
    rilis = ''
    try:
        rilis = soup.find("div", string='Published on').find_next_sibling().text
        #print(pub_date)
    except AttributeError:
        rilis = '-'
    
    publisher = soup.find("div", string='Publisher').find_next_sibling().text
    
    language = soup.find("div", string='Language').find_next_sibling().text
    
    compatible = soup.find("div", string='Best for').find_next_sibling().text
    
    # genre_mentah = soup.find("div", string='Genres').find_next_sibling().text
    # genre_semi = genre_mentah.split('/')
    # category = [x.strip(' ') for x in genre_semi]
    genre = input("masuk kateori apa: ")
    
    harga_1 = soup.select('button[class="LkLjZd ScJHi HPiPcc IfEcue"]  meta[itemprop="price"]')[0]['content'].replace('$','')
    harga_2 = float(harga_1) * 14266.00
    harga = 'Rp ' + "{:,}".format(int(harga_2)) + ',00'
 
    _rating = soup.select('div[class="BHMmbe"]')
    rating = _rating[0].getText()

    _jumlah_rating = soup.select('span[class="EymY4b"] span')
    ratingsum = _jumlah_rating[1].getText()
    

    book_info = {
        'cover_image':cover_image,
        'title':title,
        'author':author,
        'id':id,
        'slug':slug,
        'summary':summary,
        'publisher':publisher,
        'rilis':rilis,
        'language':language,
        'halaman':halaman,
        'compatible':compatible,
        'genre':genre,
        'harga':harga,
        'rating':rating,
        'ratingsum':ratingsum
    }
    # print(book_info)
    return book_info

def scrape_book(request):
    #scrapelink = Request()
    #if request.method == 'POST':
    #    scrapelink = CreateUserForm(request.POST)
    #    if scrapelink.is_valid():
    #        scrapelink.save()
    #        messages.info(request, "Sukses!")
    #    else:
    #        messages.info(request, "Invalid Credentials")
    return render(request, 'scrape.html')

def category_detail(request, slug):
    category = Category.objects.get(slug = slug)
    return render(request, 'genre_detail.html', {'category': category})

@login_required(login_url='login')
def book_detail(request, slug):
    book = Book.objects.get(slug = slug)
    return render(request, 'book_detail.html', {'book': book})

def search_book(request):
    searched_books = Book.objects.filter(title__icontains = request.POST.get('name_of_book'))
    return render(request, 'search_book.html', {'searched_books':searched_books})

def register_page(request):
    register_form = CreateUserForm()
    if request.method == 'POST':
        register_form = CreateUserForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.info(request, "Account Created Successfully!")
            return redirect('login')
           
    return render(request, 'register.html', {'register_form': register_form})

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Invalid Credentials")
        
    
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    return redirect('home')
    