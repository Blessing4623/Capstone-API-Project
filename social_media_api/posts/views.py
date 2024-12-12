from django.shortcuts import render
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment, Like
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import LikeSerializer
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class CreatePostView(generics.CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
class UpdatePostView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
class ListPostView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
class DeletePostView(generics.DestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

class CreateCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
class UpdateCommentView(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
class ListCommentView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
class DeleteCommentiew(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset= Post.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset= Comment.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class FeedView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)

class LikeView(generics.GenericAPIView):
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk=None, *args, **kwargs):
        serializer = LikeSerializer(data= request.data)
        if serializer.is_valid():
            like, created = Like.objects.get_or_create(user_id=request.user.id, post_id=pk)
            post = Post.objects.get(id=pk)
            user2_id = post.author.id
            content_type = ContentType.objects.get_for_model(Post)
            user = User.objects.get(user_id=request.user.id)
            user2 = User.objects.get(user_id=user2_id)
            if created:
                
                notification = Notification.objects.create(
                    recipient=user2,
                    actor= user,
                    content_type = content_type,
                    object_id = post,
                    verb = f'{user} liked your post',
                )
                return Response({'message': 'You have liked this post'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'You have already liked this post'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status= status.HTTP_404_NOT_FOUND)
class UnlikeView(generics.GenericAPIView):
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated]
    def post(self, request, pk=None, *args, **kwargs):
        try:
            like = Like.objects.get(user=request.user, post_id=pk)
            like.delete()
            post = Post.objects.get(id =pk)

            content_type = ContentType.objects.get_for_model(Post)
            notification = Notification.objects.filter(
                recipient = post.author,
                actor = request.user,
                content_type = content_type,
                object_id = post,
                verb = f'{request.user} liked your post',
            )
            notification.delete()
            return Response({'message': 'you unliked this post'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'message': 'You didnt like this post'}, status=status.HTTP_404_NOT_FOUND)
