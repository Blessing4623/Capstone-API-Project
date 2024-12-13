from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, bio=None, profile_picture=None, followers=None, **extra_fields):
        user = self.model(
            email = self.normalize_email(email),
            bio = bio,
            profile_picture = profile_picture,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user 

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=1000000, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='media/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='being_followed', blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='following_others', blank=True)
    
    objects = CustomUserManager()