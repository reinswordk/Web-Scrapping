from multiprocessing import context
from unicodedata import category
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from requests.sessions import Request

import bookapp
from .models import Book, Category, Todo, CSV
from django.contrib.auth.forms import UserCreationForm
from  .forms import CreateUserForm, uploadd, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

import requests
from bs4 import BeautifulSoup

from django.utils.text import slugify
import string
import random

from pymongo import MongoClient
import pymongo
import csv
from .forms import InputBuku

import datetime

def get_dbconnection():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/') 
    mydb = myclient['latscrapdb']
    mycol = mydb['bookapp_book'] 
    
    return mycol

def save_data(masukin):
    mycol = get_dbconnection()
    var_in = mycol.insert_one(masukin)
    return var_in
    

# Create your views here.
def home(request):
    recommended_books = Book.objects.filter(recommended_books = True)
    best_seller = Book.objects.filter(best_seller = True)
    diskon_books = Book.objects.filter(diskon_books = True)
    return render(request, 'home.html', {'recommended_books': recommended_books,
    'best_seller': best_seller, 'diskon_books': diskon_books
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
    
    genre_mentah = soup.find("div", string='Genres').find_next_sibling().text
    genre_semi = genre_mentah.split('/')
    genre = [x.strip(' ') for x in genre_semi]
    # genre = input("masuk kateori apa: ")
    
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
    try:
        title = request.POST['title']
        todo = Todo(title=title)
        # print(todo)
        scrap_googlebook(todo)
        save_data(book_info)
        messages.success(request, f'New Book has been added!')
        return render(request, 'scrape.html')
    except:
        return render(request, 'scrape.html')
    # return render(request, 'scrape.html')

def import_csv(filename):
    global book_info_csv
    with open(filename, 'r') as csvfile:
	
        csvreader = csv.reader(csvfile)
        
        book_info_csv = {rows[0]:rows[1] for rows in csvreader}
    return book_info_csv

def importCSV(request):
    if request.method == "FILES":
        importCSV = uploadd(request.FILES)
        if importCSV.is_valid():
            importCSV = request.FILES['upload']
            vsc = CSV(importCSV=importCSV)
            # print(todo)
            import_csv(vsc)
            save_data(book_info_csv)
            messages.info(request, "Buku berhasil ditambahkan!")
            return redirect('home')
    else:
            importCSV = uploadd()
    return render(request, 'upload.html', {'importCSV': importCSV})
    
    '''
    try:
        importCSV = request.FILES['upload']
        vsc = CSV(importCSV=importCSV)
        # print(todo)
        import_csv(vsc)
        save_data(book_info_csv)
        messages.info(request, 'Buku berhasil ditambahkan!')
        return render(request, 'uploadCSV.html')
    except:
        messages.info(request, 'Buku gagal untuk ditambahkan!')
        return render(request, 'uploadCSV.html', {'importCSV': importCSV})
    '''

def bookform(request):
  if request.method == "POST":
    form = InputBuku(request.POST)
    if form.is_valid():
      form.save()
      book_name = form.cleaned_data.get('title')
      messages.success(request, f'{book_name} has been added!')
      return redirect('form')
  else:
      form = InputBuku()
  return render(request, 'upload.html', {'form': form})

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
    
def adminpage(request):
    items = Book.objects.all()
    items_count = items.count()

    users = User.objects.all()
    users_count = users.count()

    genres = Category.objects.all()
    genres_count = genres.count()

    context = {
        'items': items,
        'items_count': items_count,
        'users': users,
        'users_count': users_count,
        'genres': genres,
        'genres_count': genres_count,
    }
    return render(request, 'admin.html', context)

def bookadmin(request):
    items = Book.objects.all()
    items_count = items.count()

    users = User.objects.all()
    users_count = users.count()

    genres = Category.objects.all()
    genres_count = genres.count()

    if request.method == 'POST':
        form = InputBuku(request.POST)
        if form.is_valid():
            form.save()
            book_name = form.cleaned_data.get('title')
            messages.success(request, f'{book_name} has been added!')
            return redirect('bookadmin')
    else:
        form = InputBuku()

    context = {
        'items': items,
        'items_count': items_count,
        'users': users,
        'users_count': users_count,
        'genres': genres,
        'genres_count': genres_count,
        'form': form,
    }
    return render(request, 'bookadmin.html', context)

def bookadmin_delete(request, pk):
    item = Book.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('bookadmin')
    return render(request, 'bookdelete.html')

def bookadmin_update(request, pk):
    item = Book.objects.get(id=pk)
    if request.method=='POST':
        form = InputBuku(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('bookadmin')
    else:
        form = InputBuku(instance=item)
    context={
        'form':form,
    }
    return render(request, 'bookupdate.html', context)

def useradmin(request):
    items = Book.objects.all()
    items_count = items.count()

    users = User.objects.all()
    users_count = users.count()

    genres = Category.objects.all()
    genres_count = genres.count()

    if request.method == 'POST':
        form = InputBuku(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bookadmin')
    else:
        form = InputBuku()

    context = {
        'items': items,
        'items_count': items_count,
        'users': users,
        'users_count': users_count,
        'genres': genres,
        'genres_count': genres_count,
        'form': form,
    }
    return render(request, 'useradmin.html', context)

def useradmin_delete(request, pk):
    user = User.objects.get(id=pk)
    if request.method=='POST':
        user.delete()
        return redirect('useradmin')
    return render(request, 'userdelete.html')

def map_genres(books):
    genres = []

    for book in books:
        for genre in book['genres']:
            genres.append(genre)
    
    genres_distinct = list(set(genres))
    result = []

    for genre in genres_distinct:
        o = {
            "label": genre,
            "value": genres.count(genre)
        }

        result.append(o)
    
    def sort_by_value(r):
        return r['value']

    result.sort(key=sort_by_value, reverse=True)
    return result[0:5]

#Fungsi Sorting

def hightolow(request):
    books = Book.objects.order_by('-rating')

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def lowtohigh(request):
    books = Book.objects.order_by('rating')

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def priceless(request):
    books = Book.objects.order_by('-harga')

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def pricey(request):
    books = Book.objects.order_by('harga')

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def newest(request):
    books = Book.objects.order_by('rilis')

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def oldest(request):
    books = Book.objects.order_by('-rilis')

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

#Fungsi Filtering

def english(request):
    books = Book.objects.filter(language__icontains="English")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def indonesian(request):
    books = Book.objects.filter(language__icontains="Indonesian")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def other(request):
    books = Book.objects.filter(language__icontains="Other")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

#Fungsi Filtering Menu Bar

def art(request):
    books = Book.objects.filter(genre__icontains="Art")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def education(request):
    books = Book.objects.filter(genre__icontains="Education")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def family(request):
    books = Book.objects.filter(genre__icontains="Family")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def fiction(request):
    books = Book.objects.filter(genre__icontains="Fiction")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def food(request):
    books = Book.objects.filter(genre__icontains="Food")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def horror(request):
    books = Book.objects.filter(genre__icontains="Horror")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def kesehatan(request):
    books = Book.objects.filter(genre__icontains="Kesehatan")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def komputer(request):
    books = Book.objects.filter(genre__icontains="Komputer")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def komik(request):
    books = Book.objects.filter(genre__icontains="Comics")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)

def sejarah(request):
    books = Book.objects.filter(genre__icontains="Sejarah")

    context = {
        'books': books
    }
    return render(request, 'all_books.html', context)