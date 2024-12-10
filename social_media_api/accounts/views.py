from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .serializers import UserSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
            if user.is_valid:
                user1 = get_user_model().objects.get(username = user.username)
                token = Token.objects.create(user=user1)
                token.save()