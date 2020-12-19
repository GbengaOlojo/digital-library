from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Book, BookInstance, Author, RentedBook
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json 

# Create your views here.
@login_required
def user_profile(request):
    user_rented_books = RentedBook.objects.filter(user=request.user).order_by('-pk')
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

@login_required
def rent_book(request, pk):
    user = request.user
    book_in_view = get_object_or_404(Book, pk=pk)
    exisiting_record =  RentedBook.objects.filter(book=book_in_view)

    if exisiting_record.count() > 0:
        messages.error(
            request, 
            f'Book [{book_in_view}] cannot be rented twice'
        )
        return redirect(reverse_lazy('user-profile'))

    RentedBook().user_rentbook(user=user, book_id=pk)

    return redirect(reverse_lazy('user-profile'))

@login_required
def return_book(request, book_instance):
    user = request.user
    
    rented_book = RentedBook.objects.filter(book_instance=book_instance).last()
    if return_book.count() < 1:
        raise Http404('Rented book can not be found')
    rented_book =rented_book.last
 
    rented_book.user_return_book(user=user)

    messages.success(
        request, 
        f'Book [{rented_book.book_instance.book}] returned successfully')

    return redirect(reverse_lazy('user-profile'))

def rent_status(self, user, book_id):
    date_rented = timezone.now()
    days_running = 0         # numbers of days the book instance or book id has been running
    
    if RENT_BOOK_STATUS =='ru' :
        date_rented += days_running
        return render(request, 'catalog/book_detail.html', {"book_id":days_running})


# reminds user to return book within a day 
def penul_rem(self):
    if book_id.days_running == 6:
        return render(request, 'catalog/book_detail.html', {"book_id":days_running})


# notifies user to return book same day 
def return_today(self):
    if book_id.days_running == 7:
        return render(request,'catalog/book_detail.html', {"book_id":due_back})
 
       
# where due day is elapsed by a day, it will increament days_running 
def book_overdue(self):
    if book_id.days_running > 7 :
        date_rented += days_running
        return render(request,'catalog/book_detail.html',{'book_id': book_id})
    

# where the days have elapsed more than 30 days, user profile is suspended 
def one_month_overdue(self):
    if book_id.days_running > 30 :
        user_profile.save(update_fields=[
            'suspended',
            'reinstated'
        ])
        return render(request,'catalog/book_detail.html',{'user_profile': suspended})


# when the user returns the book, user profile is reinstated
def book_returned(self):
    if RENT_BOOK_STATUS == 're':
        user_profile.save(update_fields=[
            'suspended',
            'reinstated'
        ])
        return render (request,'cataloq/book_detail.html',{'user_profile' : reinstated})
        

        # else, the book is available to rent
def book_available(self):
    return render (request,'cataloq/book_detail.html' ,{'book_id' : Available})
