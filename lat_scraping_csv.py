
from itertools import tee
from typing import Text
import requests

from pymongo import MongoClient
import pymongo
import csv

import requests
from bs4 import BeautifulSoup

from django.utils.text import slugify
import string
import random

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
    
        
def print_data(mycol):
    #mycol = get_dbconnection
    for x in mycol.find():
        print(x)

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

def rand_slug1():
    return ''.join(str(random.randint(0, 9)) for _ in range(8))

def scrap_googlebook(request):
    global book_info
    urlnya = request
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

def import_csv(filename):
    global book_info_csv
    with open(filename, 'r') as csvfile:
	
        csvreader = csv.reader(csvfile)
        
        book_info_csv = {rows[0]:rows[1] for rows in csvreader}
    return book_info_csv

def main():
    choice = input("mau (s)scraping atau (c)import csv: ")
    if choice == 's':
        alamat = input('Masukan URL buku: ')
        scrap_googlebook(alamat)
        
        save_data(book_info)
        print("Berhasil, cek database wis mlebu rung")
        # mycol = get_dbconnection()
        # # print_data(mycol)
    else:
        file_csv = "databuku_example.csv"
        import_csv(file_csv)
        save_data(book_info_csv)
        print("Berhasil, cek database wis mlebu rung")
       
          
if __name__ == '__main__':
    main()