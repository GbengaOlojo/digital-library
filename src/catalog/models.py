from django.db import models
from django.urls import reverse # 'reverse used to generate URLs by returning a url pattern that matches that instance 
import uuid # for generating unique ID
from django.contrib.auth.models import User 
from .errors import BookDoesNotExist, BookNotAvailable
from django.utils import timezone
from .errors import UserReantalConflictError
import json 

# Create your models here.
class Book(models.Model):
    """ Model represetation for a book """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a  brief description about the book")
    isbn = models.CharField("ISBN",max_length=13, unique=True, help_text='13 characters that identifies a book')
    genres = models.ManyToManyField('Genre', help_text=" Select a genre for this book")
    language = models.ManyToManyField('Language', help_text= 'Select the language for your book')
    image = models.URLField(null=True)

 


    def __str__(self):
        """ This string represent the Model Object """
        return f'{self.title} ({self.author})'

    def get_absolute_url(self):
        """ This returns a URL to access a book """
        return reverse('book-detail', args=[str(self.id)])

class RentedBook(models.Model):
    RENT_BOOK_STATUS = (
        ('ru',  'Running'),
        ('re', 'Returned') 

    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, null=True)
    book_instance = models.ForeignKey('BookInstance', on_delete=models.PROTECT)
    status = models.CharField(max_length=2, choices=RENT_BOOK_STATUS)
    
    def user_return_book(self,user):
        if user != self.user:
           raise UserReantalConflictError(book_instance=self.book_instance)
        else:
            #if rented book status is running 
            if self.status == "ru":
                # get &update book instance
                instance = BookInstance.objects.get(id=self.book_instance.id)
                # update
                instance.status = 'a' # available
                instance.save(update_fields=['status'])

                #UPDATE USER RENTED BOOK PROFILE
                self.status = 're' # returned 
                self.save(update_fields=['status'])

            #GENERICALLY RETURN SUCCESS (If no error is encountered)
            return json.loads('{"status": "success"}')

    
    @classmethod
    def user_rentbook(cls, user, book_id):
        """ This method calls updates a Book_Instance model from (rent --> Returns)"""

        try:
            # GET BOOK
            book= Book.objects.get(id=book_id)

            # check for available book instance 
            available_book_instances = BookInstance.objects.filter(book=book, status='a').order_by("-pk")

            if available_book_instances.count() > 0: 

                # Available
                # select the First
                book_instance = available_book_instances[0]

                #update Book Instance to loan
                book_instance.status = 'o'

                # Due Back in a week (==> 7days)
                book_instance.due_back = timezone.now() + timezone.timedelta(days=7)
                book_instance.save(update_fields=[
                    'status',
                    'due_back'
                ])
                # Create rented Book
                rented_book = cls.objects.create(status='ru', user=user, book=book, book_instance=book_instance)
                return rented_book
            
            else:
                raise BookNotAvailable(book_title=book.title, book_id=book_id)

        except Book.DoesNotExist:
            raise BookDoesNotExist(book_id=book_id)


    def __str__(self):
        return f"{self.book_instance}"


class BookInstance(models.Model):
    """ Model reprensentation for a specific copy of a book """
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'on-loan'),
        ('a', 'available')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="unique ID for this specific copy of the books across the library")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=LOAN_STATUS, default='m', help_text='Book availability')

    class Meta:
        ordering = ['due_back']
    def __str__(self):
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """ Models reprenting an Author """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image=models.URLField(null=True)
    bio =models.TextField(null=True)
    email = models.EmailField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id),f"{self.first_name.lower()}-{self.last_name.lower()}"])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Genre(models.Model):
    """ Models representing a book genre"""
    name = models.CharField(max_length=100, help_text='enter a book a genre (e.g. romance, fictions)')

    def __str__(self):
        return self.name 

class Language(models.Model):
    """ This model represents the language books are written in """
    name = models.CharField(max_length=100, help_text='enter a  language')


    def __str__(self):
        return self.name 

    