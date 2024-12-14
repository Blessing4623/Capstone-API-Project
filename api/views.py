from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import status
from .models import Movie, CastAndCrew, Review
from rest_framework.response import Response
from .serializers import MovieSerializer, CastAndCrewSerializer, ReviewSerializer, MovieListSerializer
# Create your views here.
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]
    def list(self, request, *args, **kwargs):
            movies = self.get_queryset()
            serializer = MovieListSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request, *args, **kwargs):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get', 'post'], url_path='reviews')
    def movie_reviews(self, request, pk=None):
        if request.method =="GET":
            reviews = Review.objects.filter(movie_id = pk)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                review = serializer.save(movie_id=pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)