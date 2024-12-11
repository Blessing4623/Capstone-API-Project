from django.urls import path, include
from .views import UserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register(r'', UserViewSet, basename='accounts')
urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', obtain_auth_token, name='token'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register')
]
