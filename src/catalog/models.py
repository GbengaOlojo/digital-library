from django.db import models
from django.urls import reverse # 'reverse used to generate URLs by returning a url pattern that matches that instance 
import uuid # for generating unique ID

# Create your models here.
class Book(models.Model):
    """ Model represetation for a book """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True) # Books have M21 relationship with
    summary = models.TextField(max_length=1000, help_text="Enter a  brief descriotion about the book")
    isbn = models.CharField("ISBN",max_length=13, unique=True, help_text='13 characters that identifies a book')
    genres = models.ManyToManyField('Genre', help_text=" Select a genre for this book")
    language = models.ManyToManyField('Language', help_text= 'Select the language for your book')


    def __str__(self):
        """ This string represent the Model Object """
        return self.title

    def get_absolute_url(self):
        """ This returns a URL to access a book """
        return reverse('book.detail', args=[str(self.id)])


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
    email = models.EmailField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-details', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Genre(models.Model):
    """ Models representing a bokk genfre"""
    name = models.CharField(max_length=100, help_text='enter a book a genre (e.g. romance, fictions)')
    
    def __str__(self):
        return self.name 

class Language(models.Model):
    """ This model represents the language books are written in """
    name = models.CharField(max_length=100, help_text='enter a  language')


    def __str__(self):
        return self.name 

    