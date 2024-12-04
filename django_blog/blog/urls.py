from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, profile_edit_view, profile_view, PostCreateView
from .views import PostUpdateView, PostDeleteView, PostListView, PostDetailView
from django.shortcuts import redirect

# create your urls here
urlpatterns = [
    path('login/', LoginView.as_view(template_name='blog/login.html', success_url='profile/'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login/'), name='logout' ),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile_edit/', profile_edit_view, name='profile_edit'),
    path('posts/', PostListView.as_view(), name='posts' ),
    path('post/new/', PostCreateView.as_view(), name='new_post'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]

