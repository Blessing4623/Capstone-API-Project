from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .admin_view import admin_view
from .librarian_view import librarian_view
from .member_view import member_view
urlpatterns= [
    path('book/', list_books, name='list_books'),
    path('library/', LibraryDetailView.as_view(), name='library'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/login.html'), name='logout'),
    path('register/', views.register.as_view(), name='register'),
    path('admin/', admin_view, name='admin'),
    path('librarian/', librarian_view, name='librarian'),
    path('member/', member_view, name='member'),
    path('add/', views.add_view, name='add_book'),
    path('change/', views.change_view, name='change_book'),
    path('delete/', views.delete_view, name='delete_book')
]