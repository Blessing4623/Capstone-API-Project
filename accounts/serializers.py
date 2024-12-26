from rest_framework import serializers
from .models import Like, Profile, Notification, Comment
# serializer for likes
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"

# Profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField() # defining an extra field
    class Meta:
        model = Profile
        fields = ['user', 'username', 'bio', 'date_joined', ]
    def get_username(self, obj):
        return obj.user.username # getting the users username for the profile
    

# Notifications serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
# Comments serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
# for creating comments no ones gonna type their sender name and receiver name they are done automatically
class CommentCreateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField() # Comment creaters username
    class Meta:
        model = Comment
        fields = ['comment', 'username']
    def get_username(self, obj):
        return obj.sender.username # returning the sender foreign keys name in models as the username
        
# when comments are listed they will be shown with this code
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment']