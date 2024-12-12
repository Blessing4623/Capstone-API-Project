from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .serializers import UserSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework import permissions
User = get_user_model()
CustomUser = get_user_model()
# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes =[AllowAny, IsAuthenticated]
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
            if user is not None:
                user1 = get_user_model().objects.get(username = user.username)
                token = Token.objects.get_or_create(user=user1)
                return Response({'message': 'User Logged In'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Incorrect credentials'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FollowView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = permissions.IsAuthenticated
    
    @action(detail=True, methods=['post'])
    def follow_user(self, request, user_id =None):
        try:
            target_User= User.objects.get(pk=user_id)
            if target_User != request.user:
                request.user.following.add(target_User)
                return Response({'message': f'You are now following {target_User}'}, status=status.HTTP_200_OK)
            return Response({'message': 'You cannot follow yourself'}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def unfollow_user(self, request, user_id=None):
        try:
            target_User= User.objects.get(pk= user_id)
            if target_User != request.user:
                request.user.following.remove(target_User)
                return Response({'message': f'You have unfollowed {target_User}'}, status=status.HTTP_200_OK)
            return Response({'message': 'You cannot unfollow yourself'}, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    def get_permissions(self):
        if self.action in ['follow_user', 'unfollow_user']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
