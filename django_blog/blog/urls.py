from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, profile_edit_view, profile_view, PostCreateView
from .views import PostUpdateView, PostDeleteView, PostListView, PostDetailView
from .views import CommentCreateView, CommentListView, CommentUpdateView, CommentDeleteView
from django.shortcuts import redirect
from .views import search_view, tagged_posts_view, PostBayTagListView

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
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='new_comment'),
    path('post/<int:pk>/comments/', CommentListView.as_view(), name='comments'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('search/', search_view, name='search'),
    path('tags/<slug:tag_slug>/', PostBayTagListView.as_view(), name='tags')
]

