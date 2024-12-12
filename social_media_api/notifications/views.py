from django.shortcuts import render
from rest_framework import generics
from .serializers  import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Notification
# Create your views here.
class NotificationView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = IsAuthenticated