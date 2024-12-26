from django.shortcuts import render, get_object_or_404
import requests
from datetime import datetime
from .filters import ReviewFilter
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework import status
from .models import Movie, CastAndCrew, Review
from .serializers import ReviewList2Serializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import MovieNotFoundReviewSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import MovieSerializer, CastAndCrewSerializer, ReviewSerializer, MovieListSerializer, UserSerializer, ReviewListSerializer, MovieCreateSerializer
# Create your views here.

# this function is for getting the cast and crew via omdb api
def fetch_cast_and_crew(movie_title):
    api_key = '7d9a0695'
    url = f'https://www.omdbapi.com/?t={movie_title}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cast_and_crew = []
        actors = data.get('Actors', '').split(', ') # getting the actors and seperating via commas
        for actor in actors:
            cast_and_crew.append({'name': actor, 'role': 'Actor'}) # adding all the actors
        directors = data.get('Director', '').split(', ') # getting the director or directors and seperating via commas
        for director in directors:
            cast_and_crew.append({'name': director, 'role': 'Director'}) # adding the direcor or directors
        writers = data.get('Writer', '').split(', ') # getting the writer or writers and seperating via commas
        for writer in writers:
            cast_and_crew.append({'name': writer, 'role': 'Writer'}) # adding the writers
        return cast_and_crew # returning the whole list
    return []

# for getting movie details
def fetch_movie_details(movie_title):
    api_key = '7d9a0695'
    url = f'https://www.omdbapi.com/?t={movie_title}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data= response.json()
        release_date_raw = data.get('Released') # the raw data
        release_date= datetime.strptime(release_date_raw, '%d %b %Y').date() # converting to a supported format via datetime
        details= {
            'description': data.get('Plot', ''),
            'director': data.get('Director', ''),
            'genre': data.get('Genre', ''),
            'release_date': release_date
        }
        return details # returning movie details
    return Response({'message': 'An error occured with omdb pls recheck details admin'}, status=status.HTTP_400_BAD_REQUEST)

 # the whole movie viewset   
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    permission_classes = [permissions.AllowAny, permissions.IsAuthenticated, permissions.IsAdminUser]
    lookup_field = 'name'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['rating']
    search_fields = ['name', 'description', 'genre']
    # listing movies
    def list(self, request, *args, **kwargs):
            queryset = self.filter_queryset(self.get_queryset().order_by('id'))
            page = self.paginate_queryset(queryset) # pagination
            if page is not None:
                serializer = MovieListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = MovieListSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    # admin creation for movies
    def create(self, request, *args, **kwargs):
        # requesting the data via the movie create serializer
        serializer = MovieCreateSerializer(data=request.data)
        if serializer.is_valid():
            # movie is partially created with most values as null
            movie = serializer.save()
            omdb_details = fetch_movie_details(movie.name) # getting the omdb details to add as movie info
            # getting the movie details 
            movie.description= omdb_details['description'],  
            movie.director=omdb_details['director'],
            movie.genre = omdb_details['genre'],
            movie.release_date=omdb_details['release_date']
            movie.save()
            # getting cast and crew for omdb
            omdb_cast_and_crew = fetch_cast_and_crew(movie.name)
            serializer2 = MovieSerializer(movie, many=False)
            # creating the cast and crew for every member in the list
            for member in omdb_cast_and_crew:
                CastAndCrew.objects.create(name=member['name'], role=member['role'], movie=movie)
            return Response(serializer2.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # for updating the movie based on the movie name
    def update(self, request, name=None, *args, **kwargs):
        movie = Movie.objects.get(name=name)
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            movie = serializer.save()
            movie.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    # the action for getting, creating and deleting movie reviews
    @action(detail=True, methods=['get', 'post', 'delete'], url_path='reviews')
    def movie_reviews(self, request, name=None, review_id=None):
        movie = get_object_or_404(Movie, name=name)
        # when we have the get method
        if request.method =="GET":
            # if the url has a review id passed into it
            if review_id:
                reviews = get_object_or_404(Review, id=review_id, movie=movie)
                serializer = ReviewList2Serializer(reviews, many=False) # getting the reviews full details including comments
                return Response(serializer.data, status=status.HTTP_200_OK)
            # if review id was not passed
            reviews = Review.objects.filter(movie = movie).order_by('id') # ordering to make pagination
            filtered_reviews = ReviewFilter(request.GET, queryset = reviews).qs # using review filter from filters.py
            paginator = PageNumberPagination()
            paginator.page_size = 8
            page = paginator.paginate_queryset(filtered_reviews, request) # paginating the reviews
            if page is not None:
                serializer = ReviewListSerializer(page, many=True) # returning the paged reviews
                return paginator.get_paginated_response(serializer.data) # the paged serializers data
            serializer = ReviewListSerializer(filtered_reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # for creating reviews
        elif request.method == "POST":
            serializer = ReviewSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                review = serializer.save(movie=movie)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # for deleting reviews
        elif request.method == "DELETE":
            # if the user passes in the review id
            if review_id:
                user = request.user
                review = Review.objects.get(id=review_id, movie=movie)
                # ensuring the user deleting is the owner of the review
                if request.user == review.user:
                    review.delete()
                    return Response({'message': 'review has been deleted'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'you cant delete another persons review'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'message': 'you need to add the review id to delete'}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == "PUT":
            # if review id was passed
            if review_id:
                user = request.user
                review = get_object_or_404(Review, id=review_id, movie=movie)
                # checking if the user updating is the owner of the review
                if review.user != user:
                    return Response({'message':'You cant change another persons review'}, status=status.HTTP_403_FORBIDDEN)
                serializer = ReviewSerializer(review, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'You have to provide a review id'}, status=status.HTTP_400_BAD_REQUEST)
    # for cast and crew    
    @action(detail=True, methods=['get'], url_path='cast')
    def cast_and_crew_info(self, request, name=None):
        movie = Movie.objects.get(name=name)
        cast_and_crew = CastAndCrew.objects.filter(movie= movie)
        serializer = CastAndCrewSerializer(cast_and_crew, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        


    # the permissions for which actions and which methods
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'cast_and_crew_info']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['movie_reviews'] and self.request.method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['movie_reviews'] and self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['movie_reviews'] and self.request.method == 'DELETE':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['movie_review'] and self.request.method == 'PUT':
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create']:
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action in ['retrieve'] and self.request.method == 'DELETE':
            self.permission_classes = [permissions.IsAdminUser]
        elif self.request.method == 'PUT' and self.action in ['update']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
    # for the serializer classes
    def get_serializer_class(self):
        if self.action in ['list']:
            return MovieListSerializer
        elif self.action in ['retrieve', 'create']:
            return MovieSerializer
        elif self.action in ['movie_reviews']:
            return ReviewSerializer
        elif self.action in ['cast_and_crew_info']:
            return CastAndCrewSerializer
        else:
            return MovieSerializer
        
    # for search fields
    def get_search_fields(self):
        if self.action in ['list']:
            self.search_fields= ['name', 'description', 'rating']
        if self.action in ['movie_reviews']:
            self.search_fields= ['rating']
        if self.action in ['cast_and_crew_info']:
            self.search_fields= None
        return super().get_search_fields()

# user creation view
class UserCreateView(generics.CreateAPIView):
     serializer_class = UserSerializer
     queryset = User.objects.all()
     permission_classes = [permissions.AllowAny]
# user delete view for admin
class UserDestroyView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [permissions.IsAdminUser]

# user list view for admin
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]

# for users to create reviews if movie is not found
class MovieNotFoundReviewView(generics.GenericAPIView):
    serializer_class = MovieNotFoundReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = MovieNotFoundReviewSerializer(data=request.data)
        if serializer.is_valid():
            # getting from serializer and omdb api
            title = serializer.validated_data['movie_title']
            api_key = '7d9a0695'
            url = f'https://www.omdbapi.com/?t={title}&apikey={api_key}'
            response = requests.get(url)
            # getting the title
            if response.status_code == 200:
                data = response.json()
                titles = None
                Title = data.get('Title', '').split(', ')
                for title in Title:
                    titles = title
                movie_name = titles
                # if movie is not none
                if movie_name != None and movie_name != "":
                    try:
                        movies= Movie.objects.get(name=movie_name)
                        return Response({'message':f'movie exists in the api create a post request for api/movies/{movies.name}/reviews/'}, status=status.HTTP_400_BAD_REQUEST)
                    except Movie.DoesNotExist:
                        # creates the movie and review for the movie created
                        omdb_details = fetch_movie_details(movie_name) 
                        description= omdb_details['description'],  
                        director=omdb_details['director'],
                        genre = omdb_details['genre'],
                        release_date=omdb_details['release_date']
                        Movie.objects.create(
                            name = movie_name,
                            description = description,
                            genre = genre,
                            director = director,
                            release_date = release_date
                        )
                        movie = get_object_or_404(Movie, name=movie_name)
                        omdb_cast_and_crew = fetch_cast_and_crew(movie_name)
                        for member in omdb_cast_and_crew:
                            CastAndCrew.objects.create(name=member['name'], role=member['role'], movie=movie)
                        review = Review.objects.create(
                            movie= movie,
                            review_content = serializer.validated_data['review_content'],
                            user = request.user,
                            rating = serializer.validated_data['rating']
                        )
                        review.save()

                        serializer2 = ReviewListSerializer(review, many=False)
                        return Response(serializer2.data, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'movie not found please recheck the movie title'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'movie not found please recheck title'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    