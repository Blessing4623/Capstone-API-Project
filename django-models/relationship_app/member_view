from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test


def member_view(request):
    return HttpResponse('Admin')
def is_member(user):
    return user.UserProfile.role == 'Admin'
member_view = user_passes_test(is_member)(member_view)