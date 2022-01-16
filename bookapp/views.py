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
import pymongo
from bs4 import BeautifulSoup

from django.utils.text import slugify
import string
import random

from .models import Book
from .forms import InputBuku, Scrape

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

def get_dbconnection():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/') #link mongoDB, note: koneksikan terlebih dahulu
    mydb = myclient['latscrapdb'] #gantinama database kalian, kalau belum ada/belum buat bisa langsung dibuat disini contoh => mydb = myclient['databaseku']

    mycol = mydb['bookapp_book'] #nama collection atau table, kalau belum ada lakukan sama seperti sebelumnya
    
    return mycol


# print(var_in.inserted_id)
def save_data(masukin):
    mycol = get_dbconnection()
    var_in = mycol.insert_one(masukin)
    return var_in

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

def rand_slug1():
    return ''.join(str(random.randint(0, 9)) for _ in range(8))

'''
def scrap_googlebook(request, url):
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
    '''


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

def scrape_book(request):
    if request.method == "POST":
        scrape = Scrape(request.POST)
        if scrape.is_valid():
            global book_info
            urlnya = request.POST['link']
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
                # 'genre':genre,
                'harga':harga,
                'rating':rating,
                'ratingsum':ratingsum
            }
            # print(book_info)
            scrape.save(book_info)
            messages.info(request, "Buku berhasil ditambahkan!")
            return book_info
    else:
        scrape = Scrape()
    return render(request, 'scrape.html', {'scrape': scrape})

def bookform(request):
  if request.method == "POST":
    form = InputBuku(request.POST)
    if form.is_valid():
      form.save()
      messages.info(request, "Buku berhasil ditambahkan!")
      return redirect('home')
  else:
      form = InputBuku()
  return render(request, 'upload.html', {'form': form})
