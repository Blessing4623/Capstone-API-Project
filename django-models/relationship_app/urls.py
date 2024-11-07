from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import RegisterView
from .views import LoginView
from .views import LogoutView
urlpatterns= [
    path('book/', list_books, name='list_books'),
    path('library/', LibraryDetailView.as_view(), name='library'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]