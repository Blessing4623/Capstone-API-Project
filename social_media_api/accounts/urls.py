from django.urls import path, include
from .views import UserViewSet, FollowView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register(r'', UserViewSet, basename='accounts')
urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', obtain_auth_token, name='token'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('/follow/<int:user_id>/', FollowView.as_view({'post': 'follow_user'}), name='follow'),
    path('/unfollow/<int:user_id>/', FollowView.as_view({'post': 'unfollow_user'}), name='unfollow')
]
