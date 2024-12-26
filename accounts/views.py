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

# The view for liking
class LikeView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    # post for creating a like using /like/ endpoint
    def post(self, request, title=None, review_id=None):
        # getting the movies and review using the title and review id in the url
        # if error will show standard 404 error
        movie = get_object_or_404(Movie, name=title)
        review = get_object_or_404(Review, id=review_id, movie=movie)
        # the reciever of the like has to be the one who created the review
        receiver = review.user
        # creating the like or getting if not created
        like, created = Like.objects.get_or_create(review=review, sender=request.user, receiver=receiver)
        # if it was created and not gotten in case user has already liked
        if created:
            # creating the notification for the user who made the review to know that is review was liked
            notification = Notification.objects.create(
                user=receiver,
                message=f"{request.user} liked your review with id {review_id} for the movie {movie.name}."
            )
            return Response({'message': 'You have liked this review'}, status=status.HTTP_201_CREATED)
        # if the user has already liked
        else:
            return Response({'message': 'You have already liked this post'}, status=status.HTTP_200_OK)
        
    
# unlike view
class UnlikeView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    # post for unliking
    def post(self, request, title=None, review_id=None):
        # getting movie and review via url
        movie = get_object_or_404(Movie, name=title)
        review = get_object_or_404(Review, id=review_id, movie=movie)
        # implementing logic in case user did not like and wants to unlike
        try:
            like = Like.objects.get(review=review, sender=request.user)
            like.delete()
            return Response({'message': 'You have unliked this post'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'message': 'You did not like this post'}, status=status.HTTP_404_NOT_FOUND)
        
    

# user profile view
class ProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    # shows the user profile
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # to edit the user profile maybe the bio and others
    def put(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile= serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # if the user wants to delete his account from the api he can run this deletes the user and also the profile
    def delete(self, request):
        user = User.objects.get(request.user)
        user.delete()
        return Response({'message': 'Your profile has been deleted'})
    
# if you want to view another users profile via the users id number
class ProfileDetailView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, user_id=None):
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# For getting your notifications
class NotificationListView(generics.GenericAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# commenting on a review
class CommentView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    # post for creating a comment
    def post(self, request, title=None, review_id=None):
        # will ask for users comment
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            # getting the movie and review via url
            movie = get_object_or_404(Movie, name=title)
            review = get_object_or_404(Review, id=review_id, movie=movie)
            # the receiver being the one who made the review
            receiver = review.user
            # the comment being created
            comment = Comment.objects.create(review=review, sender=request.user, receiver=receiver, comment=serializer.validated_data['comment'])
            # creating the notification
            notification = Notification.objects.create(
                user=receiver,
                message=f"{request.user} commented on your review with id {review_id} for the movie {movie.name}."
            )
            return Response({'message': 'You have commented on this review'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_200_OK)
    # to get all comments for a review    
    def get(self, request, title=None, review_id=None):
        movie = get_object_or_404(Movie, name=title)
        review = get_object_or_404(Review, id=review_id, movie=movie)
        comment = Comment.objects.filter(review=review)
        serializer = CommentListSerializer(comment, many=True)
        # implementing logic if there are no comments
        try:
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'message': 'No comments to show'}, status=status.HTTP_200_OK)
# for deleting comments       
class CommentEditView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    # delete for deleting
    def delete(self, request, title=None, review_id=None, comment_id=None):
        movie = get_object_or_404(Movie, name=title)
        review = get_object_or_404(Review, id=review_id, movie=movie)
        # logic for deleting comments if they exist
        try:
            comment = Comment.objects.get(id=comment_id, review=review, sender=request.user)
            comment.delete()
            return Response({'message': 'You have deleted this comment'}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'message': 'You did not comment on this review'}, status=status.HTTP_404_NOT_FOUND)
    # editing comments
    def put(self, request, title=None, review_id=None, comment_id=None):
        movie = get_object_or_404(Movie, name=title)
        review = get_object_or_404(Review, id=review_id, movie=movie)
        try:
            comment = Comment.objects.get(id=comment_id, review=review, sender=request.user)
            serializer = CommentCreateSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response({'message': 'You did not comment on this review'}, status=status.HTTP_400_BAD_REQUEST)
        