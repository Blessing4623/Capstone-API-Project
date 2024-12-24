from rest_framework import serializers
from .models import Like, Profile, Notification, Comment

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['user', 'username', 'bio', 'date_joined', ]
    def get_username(self, obj):
        return obj.user.username
    


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class CommentCreateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['comment', 'username']
    def get_username(self, obj):
        return obj.sender.username
        

class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment']