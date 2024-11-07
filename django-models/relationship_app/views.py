from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
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