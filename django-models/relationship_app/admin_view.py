from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test


def admin_view(request):
    return HttpResponse('Admin')
def is_admin(user):
    return user.UserProfile.role == 'Admin'
admin_view = user_passes_test(is_admin)(admin_view)