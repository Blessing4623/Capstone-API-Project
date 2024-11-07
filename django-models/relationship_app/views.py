from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Library
# Create your views here.

def list_books(request):
    book = Book.objects.all()
    return render('relationship_app/list_books.html')
class LibraryDetailView(DetailView):
    model_name = Library
    template_name = 'library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.objects.books.all()
        return context