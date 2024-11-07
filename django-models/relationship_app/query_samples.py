from .models import Book, Author, Library, Librarian

books_by_author = Book.objects.filter(author="")
all_books = Book.objects.all()
Librarian_books = Book.objects.get(library="")