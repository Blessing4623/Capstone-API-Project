from django.urls import path, include
from .views import MovieViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movies')

urlpatterns = [
    path('', include(router.urls)),
]
