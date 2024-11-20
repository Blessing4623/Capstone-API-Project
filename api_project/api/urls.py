from django.urls import path
from .views import BookList

# creating a url pattern for the api
urlpatterns = [
    path('books/', BookList.as_view(), name='book-list')
]
