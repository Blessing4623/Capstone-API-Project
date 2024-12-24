from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=3000)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=1000, null=True, blank=True)
    director = models.CharField(max_length= 3000, null=True, blank=True)
    rating = models.DecimalField(
        max_digits= 3,
        decimal_places= 1,
        validators =[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ],
        null= True,
        blank=True
    )

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_review')
    rating = models.DecimalField(
        max_digits= 3,
        decimal_places= 1,
        validators =[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ]
    )
    review_content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, null=True)

class CastAndCrew(models.Model):
    name = models.CharField(max_length=10000)
    role = models.CharField(max_length=1000)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='cast_and_crew')