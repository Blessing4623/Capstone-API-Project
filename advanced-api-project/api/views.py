from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
# Create your views here.
class ListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['title', 'author']
    ordering_fields = "__all__"
    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        if title:
            return Book.objects.filter(title=title)
class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class UpdateView(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    def perform_update(self, serializer):
        serializer.save()
class DeleteView(generics.RetrieveDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]