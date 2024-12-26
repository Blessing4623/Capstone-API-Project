from rest_framework import serializers
from .models import Movie, Review, CastAndCrew
from accounts.models import Like, Comment
from django.contrib.auth.models import User
from accounts.serializers import CommentCreateSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'error_messages':{'required': 'Yoou have to provide a password'}},
            'email': {'required': True, 'error_messages': {'required': 'You have to provide an email'}},
            'username': {'required': True, 'error_messages': {'required': 'You have to provide a username'}}
        }
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'review_content', 'rating']
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        return Review.objects.create(user=user, **validated_data)

    
class ReviewListSerializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    no_of_likes = serializers.SerializerMethodField()
    no_of_comments = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'review_content', 'rating', 'created_date', 'user', 'username', 'no_of_likes', 'no_of_comments']
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
    

class ReviewList2Serializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    no_of_likes = serializers.SerializerMethodField()
    no_of_comments = serializers.SerializerMethodField()
    comments = CommentCreateSerializer(read_only=True, many=True, source = 'review_comment')
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



class CastAndCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastAndCrew
        fields = ['name', 'role', 'movie']

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True, read_only=True)
    cast_and_crew = CastAndCrewSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'release_date', 'genre', 'director', 'rating', 'cast_and_crew', 'reviews']


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'release_date', 'genre', 'director', 'rating']

class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields= ['name', 'rating']

class MovieNotFoundReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(max_length=1000)
    class Meta:
        model = Review
        fields = ['review_content', 'rating', 'movie_title']