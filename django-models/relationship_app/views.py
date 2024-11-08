from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

def list_books(request):
    book = Book.objects.all()
    return render('relationship_app/list_books.html' {'book': book})
class LibraryDetailView(DetailView):
    model_name = Library
    template_name = 'relationship_app/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.objects.books.all()
        context['library'] = self.object
        return context

class register(CreateView):
    form_class = UserCreationForm()
    success_url = reverse_lazy('login')
    template_name = 'relationship_app/register.html'
class LoginView(login):
    template_name = 'relationship_app/login.html'
class LogoutView(logout):
    template_name='relationship_app/logout.html'

def is_admin(user):
    return user.userprofile == 'Admin'
def is_librarian(user):
    return user.userprofile == 'Librarian'
def is_member(user):
    return user.userprofile == 'Member'
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


