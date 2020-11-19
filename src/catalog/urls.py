from django.urls import path 
from .views import index 
#catalogs
#catalog/books
#catalog/authors
#catalog/books/<id: e.g 3 >
urlpatterns = [
    path('', index, name="index")
   
]



  
