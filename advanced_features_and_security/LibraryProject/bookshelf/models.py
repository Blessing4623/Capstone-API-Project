from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField(default=2000)
    class Meta:
        permissions = (can_view, can_create, can_edit, can_delete)

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(blank=True)
    profile_photo = models.ImageField(blank=True)
    objects = CustomUserManager()
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
