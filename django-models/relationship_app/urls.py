from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import RegisterView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
urlpatterns= [
    path('book/', list_books, name='list_books'),
    path('library/', LibraryDetailView.as_view(), name='library'),
    path('login/', LoginView.as_view(template_name='relationship.py/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship.py/login.html'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]