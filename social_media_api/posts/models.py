from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    title = models.CharField(max_length=3000)
    content = models.TextField(max_length=20000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='post')
    author = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comment_author')
    content= models.TextField(max_length=20000)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
