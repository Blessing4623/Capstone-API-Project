from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=10000)

class Book(models.Model):
    title = models.CharField(max_length=10000000)
    publication_year = models.IntegerField(default=2000)
    author = models.ForeignKey(Author, on_delete= models.CASCADE)
    #created a foreign key referencing the book model