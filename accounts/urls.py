from django.urls import path
from . import views

urlpatterns = [
    path('movies/<str:title>/reviews/<int:review_id>/like/', views.LikeView.as_view(), name='like'),
    path('movies/<str:title>/reviews/<int:review_id>/unlike/', views.UnlikeView.as_view(), name='unlike'),
    path('profile/', views.ProfileView.as_view(), name='user_profile'),
    path('profile/<int:user_id>/', views.ProfileDetailView.as_view(), name='profiles'),
    path('notifications/', views.NotificationListView.as_view(), name='notification'),
    path('movies/<str:title>/reviews/<int:review_id>/comment/', views.CommentView.as_view(), name='comments'),
    path('movies/<str:title>/reviews/<int:review_id>/comment/<int:comment_id>/', views.CommentDeleteView.as_view(), name='delete_comment')
]

