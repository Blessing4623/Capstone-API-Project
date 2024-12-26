from django.urls import path, include
from .views import MovieViewSet, UserCreateView, UserDestroyView, UserListView, MovieNotFoundReviewView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movies')

urlpatterns = [
    path('', include(router.urls)),
    path('token_auth/', obtain_auth_token, name='api-auth-token'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('movies/<str:name>/reviews/<int:review_id>/', MovieViewSet.as_view({'get': 'movie_reviews'}), name='review'),
    path('user/admin/delete_user/<str:username>/', UserDestroyView.as_view(), name='delete_user'),
    path('user/admin/show_users/', UserListView.as_view(), name='show_users'),
    path('review/', MovieNotFoundReviewView.as_view(), name='review')
]