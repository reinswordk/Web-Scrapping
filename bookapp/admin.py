from django.contrib import admin
from .models import Category, Book, BookSearch, MyModel, MyScrape
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookSearch)
admin.site.register(MyModel)
admin.site.register(MyScrape)
