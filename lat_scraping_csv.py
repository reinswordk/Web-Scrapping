from itertools import tee
from typing import Text
import requests

from pymongo import MongoClient
import pymongo
import csv

import requests
from bs4 import BeautifulSoup

import os
import urllib.request


def get_dbconnection():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/') #link mongoDB, note: koneksikan terlebih dahulu
    mydb = myclient['latscrapdb'] #gantinama database kalian, kalau belum ada/belum buat bisa langsung dibuat disini contoh => mydb = myclient['databaseku']

    mycol = mydb['buku'] #nama collection atau table, kalau belum ada lakukan sama seperti sebelumnya
    
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

def scrap_googlebook(url):
    global book_info
    urlnya = url
    page = requests.get(urlnya)
    soup = BeautifulSoup(page.text, 'html.parser')

    _judul = soup.select('h1[itemprop="name"] span')
    judul = _judul[0].getText()

    _penulis = soup.select('a[class="hrTbp R8zArc"]')
    penulis = _penulis[0].getText()
    
    _desc = soup.select('span[jsslot=""]')
    desc = _desc[0].getText()

    # if not os.path.exists("images"):
    #     os.makedirs("images")
    _cover = soup.find('img', 'T75of h1kAub')
    cover = _cover['src']
    # full_path = 'images/' + judul + '.jpg'
    # urllib.request.urlretrieve(cover_link, full_path)
    # loc_file = os.path.splitext('images/'+judul+'.jpg')[0]
    # loc_file_final = loc_file + '.jpg'
    # with open(loc_file_final, 'rb') as f:
    #     image = f.read()
    
    halaman = soup.find("div", string='Pages').find_next_sibling().text
    pub_date = ''
    try:
        pub_date = soup.find("div", string='Published on').find_next_sibling().text
        #print(pub_date)
    except AttributeError:
        pub_date = '-'
    
    penerbit = soup.find("div", string='Publisher').find_next_sibling().text
    
    bahasa = soup.find("div", string='Language').find_next_sibling().text
    
    kompability = soup.find("div", string='Best for').find_next_sibling().text
    
    genre_mentah = soup.find("div", string='Genres').find_next_sibling().text
    genre_semi = genre_mentah.split('/')
    genre = genre_semi
    
    harga_1 = soup.select('button[class="LkLjZd ScJHi HPiPcc IfEcue"]  meta[itemprop="price"]')[0]['content'].replace('$','')
    harga_2 = float(harga_1) * 14266.00
    harga_final = 'Rp ' + "{:,}".format(int(harga_2)) + ',00'
 
    _rating = soup.select('div[class="BHMmbe"]')
    rating = _rating[0].getText()

    _jumlah_rating = soup.select('span[class="EymY4b"] span')
    jumlah_rating = _jumlah_rating[1].getText()
    

    book_info = {
        'Cover':cover,
        'Judul':judul,
        'Penulis':penulis,
        'Deskripsi':desc,
        'Penerbit':penerbit,
        'Tanggal Terbit':pub_date,
        'Bahasa':bahasa,
        'Halaman':halaman,
        'Baik Untuk':kompability,
        'Genre':genre,
        'Harga':harga_final,
        'Rating':rating,
        'Jumlah Rating':jumlah_rating
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

