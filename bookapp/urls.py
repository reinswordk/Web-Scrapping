from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name = 'home'),
    path('all_books', views.all_books, name = 'all_books'),
    path('genre/<str:slug>', views.category_detail, name = 'category_detail'),
    path('pdf/<str:slug>', views.book_detail, name = 'book_detail'),
    path('searched_books', views.search_book, name = 'book_search'),
    path('register', views.register_page, name = 'register'),
    path('login', views.login_page, name = 'login'),
    path('logout', views.logout_user, name = 'logout'),
    path('scrape', views.scrape_book, name = 'scrape_book'),
    path('upload', views.importCSV, name = 'importCSV'),
    path('form', views.bookform, name='form'),
    path('dashboard', views.adminpage, name='adminpage'),
    path('bookadmin', views.bookadmin, name='bookadmin'),
    path('bookadmin/delete/<int:pk>/', views.bookadmin_delete, name='bookadmin-delete'),
    path('bookadmin/update/<int:pk>/', views.bookadmin_update, name='bookadmin-update'),
    path('useradmin', views.useradmin, name='useradmin'),
    path('useradmin/delete/<int:pk>/', views.useradmin_delete, name='useradmin-delete'),
]