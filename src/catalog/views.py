from django.shortcuts import render
from catalog.models import Book 

# Create your views here.
def index(request):
    """view function for the index page"""

    #numbers of books 
    num_books = Book.objects.all().count()

    #returns the html template with context data 
    return render (
        request,
        'index.html',
        context= {
            'num_books': num_books
        }
    )
