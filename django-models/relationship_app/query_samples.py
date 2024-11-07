from .models import Book, Author, Library, Librarian

books_by_author = Book.objects.filter(author=author_name)
all_books = Book.objects.all()
Librarian_books = Library.objects.get(library=library_name)