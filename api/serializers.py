from rest_framework import serializers
from .models import Movie, Review, CastAndCrew
from accounts.models import Like, Comment
from django.contrib.auth.models import User
from accounts.serializers import CommentCreateSerializer

# Numerous serializers for numerous operations

# User serializers for user registration and creation
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        # errors give django errors so I created error logic so it can show error messages
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'error_messages':{'required': 'Yoou have to provide a password'}},
            'email': {'required': True, 'error_messages': {'required': 'You have to provide an email'}},
            'username': {'required': True, 'error_messages': {'required': 'You have to provide a username'}}
        }
    # creating a user from the serializers validated data
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user

# serializer for review creation
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'review_content', 'rating']
    # automatical creation setting the user to the current user
    def create(self, validated_data):
        # in views I passed a context called request for requesting users
        request = self.context.get('request')
        user = request.user
        # creating the review
        return Review.objects.create(user=user, **validated_data)

# Listing out reviews  
class ReviewListSerializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField() # the movie title
    username = serializers.SerializerMethodField() # the username of the user who created the review
    no_of_likes = serializers.SerializerMethodField() # the no of likes for the review
    no_of_comments = serializers.SerializerMethodField() # the no of comments for the review
    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'review_content', 'rating', 'created_date', 'user', 'username', 'no_of_likes', 'no_of_comments']
    def get_movie_title(self, obj):
        return obj.movie.name # getting the movie name
    def get_username(self, obj):
        return obj.user.username # getting the username
    def get_no_of_likes(self, obj):
        likes = Like.objects.filter(review= obj).count() # counting the likes via the review
        return likes
    def get_no_of_comments(self, obj):
        comments = Comment.objects.filter(review=obj).count() # counting the comments via the review
        return comments
    
# gives full detail of reviews including comments when one review is called
class ReviewList2Serializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    no_of_likes = serializers.SerializerMethodField()
    no_of_comments = serializers.SerializerMethodField()
    comments = CommentCreateSerializer(read_only=True, many=True, source = 'review_comment') # gets all comments
    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'review_content', 'rating', 'created_date', 'user', 'username', 'no_of_likes', 'no_of_comments', 'comments']
    def get_movie_title(self, obj):
        return obj.movie.name
    def get_username(self, obj):
        return obj.user.username
    def get_no_of_likes(self, obj):
        likes = Like.objects.filter(review= obj).count()
        return likes
    def get_no_of_comments(self, obj):
        comments = Comment.objects.filter(review=obj).count()
        return comments


# cast and crew serializer
class CastAndCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastAndCrew
        fields = ['name', 'role', 'movie']

# movie serializer
class MovieSerializer(serializers.ModelSerializer):
    cast_and_crew = CastAndCrewSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'release_date', 'genre', 'director', 'cast_and_crew']

# listing out movie serializers
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'release_date', 'genre', 'director']

# admin creating a movie serializer
class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields= ['name']

# this is the serializer when a movie is not in our database
# users can create a review via the movie title and also create the movie
class MovieNotFoundReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(max_length=1000) # the movie title
    class Meta:
        model = Review
        fields = ['review_content', 'rating', 'movie_title']