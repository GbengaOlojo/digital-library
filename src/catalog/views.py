from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Book, BookInstance, Author
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def user_profile(request):
    user_rented_books = RentedBook.objects.filter(user=request.user)
    return render(
        request,
        'profile.html',
        context={
            'user': request.user,
            'rented_books':user_rented_books
        }
    )

def index(request):
    """view function for the index page"""

    #numbers of books 
    num_books = Book.objects.all().count()
    all_books = Book.objects.all().order_by('-id')

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    #returns the html template with context data 
    return render (
        request,
        'index.html',
        context= {
            'num_books': num_books,
            'books': all_books,
            'num_visits': num_visits
        }
    )


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # save user details
            form.save()
            # send sucess message
            messages.success(request, "Login to complete signup")
            return redirect(reverse_lazy('login'))
        else:
            return render(
                request,
                'registration/signup.html',
                {
                    'form':form
                }
            )
    else:
        form = UserCreationForm()
        return render(
            request, 
            'registration/signup.html',
            {
                'form': form
            }
            
        )


#class BookDetailView(generic.DetailView):
#   model = Book 

def Book_detail_view(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404('Book request cannot be found')

    #  check if book is available for rent
    copies_available = BookInstance.objects.filter(book=book, status='a').count()

    return render(
        request,
        'catalog/book_detail.html',
        context={
            'book': book,
            'copies': copies_available
        }
    )


# click on authors to view their books
def author_list_views(request):
    if request.method == 'POST':
        print(request.POST)
        search_input = request.POST.get('author', 'Empty').lower()

        # get matcing authors
        authors = Author.objects.filter(Q(first_name__icontains=search_input) | 
        Q(last_name__icontains=search_input))
    

        return render(
        request,
        'catalog/authors_list.html',
        context = {
            'authors': authors,
            'numbers_of_authors' : authors.count(),
            'search_item': search_input

           }
           
        )
    else:
        authors = Author.objects.all().order_by('first_name')
        return render(
        request,
        'catalog/authors_list.html',
        context = {
            'authors': authors,
            'numbers_of_authors' : authors.count()
        }
    )
    


def author_detail_view(request, pk, slug):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author)

    return render(
        request,
        "catalog/author_detail.html",
        context={
            "author": author,
            "books": books
    }
)