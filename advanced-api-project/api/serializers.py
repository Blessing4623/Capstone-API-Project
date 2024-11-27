from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)
    # made the author reference the model serializer class
    class Meta:
        model = Book
        fields = '__all__'
    def validate_publication_year(self, value):
        current_year = datetime.now().year()
        if value > current_year:
            raise serializers.ValidationError("Publication Year cannot be in the future")
        return value