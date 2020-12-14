from django.urls import path
from .views import index, Book_detail_view
from .views import author_list_views, author_detail_view
from .views import rent_book


#catalogs
#catalog/books
#catalog/authors
#catalog/books/<id: e.g 3 >
urlpatterns = [
    path('', index, name="index"),
    path('book/<int:pk>',Book_detail_view, name='book-detail'),
    path('authors',author_list_views, name='author-list'),
    path('author/<int:pk>/<slug:slug>', author_detail_view,name="author-detail"),

    path('rent-book/<int:pk>', rent_book, name='rent-book')
]



  
