from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy,reverse
from catalog.views import signup, user_profile, UserCreationForm
from django.contrib.auth.models import User 
#from django.urls import 
from django.http import Http404, HttpResponse, request
from django.utils import timezone
from django.test import TestCase
import json 

class BaseTest(TestCase):
    def setUp(self):
        self.index_urls=reverse('index')
        self.signup_url=reverse('signup')
        self.login_url=reverse('login')
        self.index_urls=reverse('index')
        
        self.user ={
            'email' : 'useremail@email.com',
            'username' : 'username',
            'password' : 'password',   
            'password2' : 'password',      
            
        }
 
        self.user_short_password ={
            'email' : 'useremail@email.com',
            'username' : 'username',
            'password' : 'rej',   
            'password2' : 'rej',      
        
        }

        self.user_unmatched_password ={
            'email' : 'useremail@email.com',
            'username' : 'username',
            'password' : 'ffffffff',   
            'password2' :'ffffffff',      
        
        } 

        self.existing_username = {
            'text' : 'A user with that username already exists.'
            }

        self.username ={
            'username': 'username',
            'password':'password'
        }
        
        #pls complete by assigning values.  
         self.num_books
         self.increament
        
        return super().setUp()


class RegistrationTest(BaseTest):
   
    def test_view_index_successfully(self):
        '''
        Testing the main page of our digital library to be index.html
        '''
        response = self.client.get(self.index_urls)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_user_register_successfully(self):
        response = self.client.post(self.signup_url,self.user, format='text/html')
        self.assertTrue(reverse_lazy('login'))


    def test_user_register_unsuccessful(self):
        response = self.client.post(self.signup_url,self.user_short_password , format='text/html')
        self.assertTrue(reverse_lazy('signup'))


    def test_user_entered_unmatched_password(self): 
        response = self.client.post(self.signup_url,self.user_unmatched_password, format='text/html')
        self.assertTrue(reverse_lazy('signup'))

    def test_user_existing_username(self):       
        response = self.client.post(self.signup_url, self.existing_username, format='text/html')
        self.assertTrue(reverse_lazy('signup'))


class LoginTest(BaseTest):
        """testing the functionalities of login page"""
    def test_login_page_accessed_successfully(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_successfully(self):
        """ Test case for successful login """
        self.client.post(self.signup_url,self.user, format='text/html')
        #user = User.objects.filter(username=self.user[username]).first()
        user.is_active=True
        user.save()
        response =self.client.post(self.login_url,self.user,format='text/html')
        self.assertTemplateUsed(response, 'catalog/book_detail.html')


    def test_login_page_accessed_unsuccessfully(self):
        """ Test case for unsuccessful login """
        self.client.post(self.signup_url,self.user, format='text/html')
        user.is_active=True
        user.save()
        response =self.client.post(self.login_url,self.user,format='text/html')
        if self.username != self.username and self.password != password:
            self.assertNotEqual(self.username, self.username, 
            'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            self.assertNotEqual(self.password, self.password, 
            'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def test_unregistered_user_login_unsucessful(self):
        """ Test case for unregistered users attempting login """
        response =self.client.post(self.login_url,self.user,format='text/html')
        user.is_active=False
        self.assertEqual(self.reponse, 'login.html')
  
class Index(BaseTest):
    def test_number_of_times_visited(self):
        """displays the index"""
        self.client.post('index.html')
        self.assertTemplateUsed(response, 'index.html')

    def test_popup_displayed(self):
        """testing numbers of times site visted per day by unregistered user"""
        self.client.post('index.html')
        self.assertTemplateUsed(response, 'index.html')

    def test_popup_close(self):
        """closing the popup"""
        self.client.post('index.html')
        self.num_visits.request_session=True
        self.num_visits.request_session.close()
        self.assertIsNone(content, self.num_visits.request_session = None)
        self.assertTrue(response, 'index.html')

    def test_popup_increments(self):
         """increamenting the num of times visited"""
        self.client.post('index.html')
        self.num_visits.request_session=True
        if self.client.post('index.html') :
            self.increament = self.num_visits.request_session += 1
        self.assertGreater(increament < num_visits)


    def test_all_books(self):
        """Displays all books"""
        self.client.post('index.html')
        self.num_books.Book.objects.all().count()
        self.all_books == self.num_books.len().all.count()
        self.assertEqual(self.num_book == self.all_books)
        self.assertTemplateUsed('index.html')


   


class BookTest(BaseTest):
    def book_overdue(self):
   
    def one_month_overdue(self):
    
    def book_returned(self):
 
    def book_available(self):
 
        
     
        



'''     




    def 
    

class Profile(unittest.TestCase):




 

def Book_detail_view(self:

def 
   
 
def author_list_views(request):
       
def author_detail_view(request, pk, slug):

 
def rent_book(request, pk):
   

 
def return_book(request, book_instance):
    
def rent_status(self, user, book_id):
   
def index(request):
 
def penul_rem(self):
 
def return_today(self):
 
        


'''
























































































































































if __name__ == "__main__":
    unittest.main()