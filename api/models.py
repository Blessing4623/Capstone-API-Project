from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=3000)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=1000)
    director = models.CharField(max_length= 3000)
    rating = models.DecimalField(
        max_digits= 3,
        decimal_places= 2,
        validators =[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ]
    )

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_review')
    rating = models.DecimalField(
        max_digits= 3,
        decimal_places= 2,
        validators =[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ]
    )
    review = models.TextField()

class CastAndCrew(models.Model):
    name = models.CharField(max_length=10000)
    role = models.CharField(max_length=1000)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='cast_and_crew')