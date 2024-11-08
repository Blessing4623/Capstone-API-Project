from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test


def librarian_view(request):
    return HttpResponse('Admin')
def is_librarian(user):
    return user.UserProfile.role == 'Admin'
librarian_view = user_passes_test(is_librarian)(librarian_view)