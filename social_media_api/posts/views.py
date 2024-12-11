from django.shortcuts import render
from rest_framework import generics
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import viewsets
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