from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from api.models import Review
# The Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_user')
    bio = models.TextField(blank=True)
    date_joined = models.DateField(auto_now_add=True)

# The Like Model
class Like(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="review_like")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recieved')

# The Notification Model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_user")
    message = models.TextField(max_length=30000)
    time_created = models.DateTimeField(auto_now_add=True)
# The Comment Model
class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_comment')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_sender')
    receiver =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_receiver')
    comment = models.TextField()