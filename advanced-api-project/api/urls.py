from django.urls import path
from . import views
# creating url patterns
urlpatterns = [
    path('books/', views.ListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.DetailView.as_view(), name='book_detail'),
    path('books/new/', views.CreateView.as_view(), name='book_create'),
    path('books/<int:pk>/edit', views.UpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete', views.DeleteView.as_view(), name='book_delete')
]