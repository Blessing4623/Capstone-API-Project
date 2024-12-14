from rest_framework import serializers
from .models import Movie, Review, CastAndCrew

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"

class CastAndCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CastAndCrew
        fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    cast_and_crew = CastAndCrewSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'release_date', 'genre', 'director', 'rating', 'reviews', 'cast_and_crew']


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'release_date', 'genre', 'director', 'rating']
        