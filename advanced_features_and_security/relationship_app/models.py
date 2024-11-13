from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=200)
    return self.name
class Book(models.Model):
    title = models.CharField(max_length=1000)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    return self.title
    class Meta:
        permissions = (can_add_book, can_change_book, can_delete_book)
class Library(models.Model):
    name = models.CharField(max_length=1000)
    books = models.ManyToManyField(Book)
    return self.name
class Librarian(models.Model):
    name = models.CharField(max_length=1000)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
    return self.name
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('Admin','Admin'), ('Librarian', 'Librarian'), ('Member', 'Member')])
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(blank=true)
    profile_photo = models.ImageField(blank=true)
    objects = CustomUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, date_of_birth=None, profile_photo=None):
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth= date_of_birth,
            profile_photo= profile_photo
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(self._db)
        return user