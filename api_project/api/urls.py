from django.urls import path, include
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from rest_framework.authtoken.views import obtain_auth_token
# creating a url pattern for the api
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all' )
urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
    path('api/token/', obtain_auth_token, name='api_token_auth')
]
