from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField('Categories', max_length=50)
    slug = models.SlugField(max_length = 50)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length = 100)
    slug = models.SlugField(max_length=100)
    cover_image = models.ImageField(upload_to = 'img', blank = True, null = True)
    author = models.CharField(max_length=50)
    summary = models.TextField()
    publisher = models.CharField(max_length=50)
    rilis = models.DateTimeField()
    language = models.CharField(max_length=10)
    halaman = models.CharField(max_length=10)
    compatible = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    harga = models.CharField(max_length=50)
    rating = models.CharField(max_length=3)
    ratingsum = models.CharField(max_length=3)
    category = models.CharField(max_length=50)
    pdf = models.FileField(upload_to='pdf')
    recommended_books = models.BooleanField(default=False)
    fiction_books = models.BooleanField(default=False)
    business_books = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class BookSearch(models.Model):
    name_of_book = models.CharField(max_length=100)
    def __str__(self):
        return self.name_of_book
