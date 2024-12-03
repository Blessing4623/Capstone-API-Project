from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, profile_edit_view, profile_view
from django.shortcuts import redirect

# create your urls here
urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html', success_url='profile/'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login/'), name='logout' ),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile_edit/', profile_edit_view, name='profile_edit'),
]

