from django.shortcuts import render
from rest_framework import generics
from .serializers import LikeSerializer, NotificationSerializer, ProfileSerializer, CommentSerializer, CommentCreateSerializer
from .models import Like, Notification, Profile, Comment
from .serializers import CommentListSerializer
from api.models import Review, Movie
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth.models import User
# Create your views here.


class LikeView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, title=None, review_id=None):
        movie = get_object_or_404(Movie, name=title)
        review = get_object_or_404(Review, id=review_id, movie=movie)
        receiver = review.user
        like, created = Like.objects.get_or_create(review=review, sender=request.user, receiver=receiver)
        if created:
            notification = Notification.objects.create(
                user=receiver,
                message=f"{request.user} liked your review with id {review_id} for the movie {movie.name}."
            )
            return Response({'message': 'You have liked this review'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'You have already liked this post'}, status=status.HTTP_200_OK)
        
    

class UnlikeView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, title=None, review_id=None):
        movie = get_object_or_404(Movie, name=title)
        review = get_object_or_404(Review, id=review_id, movie=movie)
        try:
            like = Like.objects.get(review=review, sender=request.user)
            like.delete()
            return Response({'message': 'You have unliked this post'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'message': 'You did not like this post'}, status=status.HTTP_404_NOT_FOUND)
        
    


class ProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile= serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProfileDetailView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, user_id=None):
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class NotificationListView(generics.GenericAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class CommentView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, title=None, review_id=None):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            movie = get_object_or_404(Movie, name=title)
            review = get_object_or_404(Review, id=review_id, movie=movie)
            receiver = review.user
            comment = Comment.objects.create(review=review, sender=request.user, receiver=receiver, comment=serializer.validated_data['comment'])
            
            notification = Notification.objects.create(
                user=receiver,
                message=f"{request.user} commented on your review with id {review_id} for the movie {movie.name}."
            )
            return Response({'message': 'You have commented on this review'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)
        
    def get(self, request, title=None, review_id=None):
        movie = get_object_or_404(Movie, name=title)
        review = get_object_or_404(Review, id=review_id, movie=movie)
        comment = Comment.objects.filter(review=review)
        serializer = CommentListSerializer(comment, many=True)
        try:
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'message': 'No comments to show'}, status=status.HTTP_200_OK)
        
class CommentDeleteView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, title=None, review_id=None, comment_id=None):
        movie = get_object_or_404(Movie, name=title)
        review = get_object_or_404(Review, id=review_id, movie=movie)
        try:
            comment = Comment.objects.get(id=comment_id, review=review, sender=request.user)
            comment.delete()
            return Response({'message': 'You have deleted this comment'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'message': 'You did not comment on this review'}, status=status.HTTP_404_NOT_FOUND)
        