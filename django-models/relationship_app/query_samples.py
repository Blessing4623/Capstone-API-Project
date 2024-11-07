from .models import Book, Author, Library, Librarian

books_by_author = Book.objects.filter(author=author_name)
library = Library.objects.get(name=library_name)
library.books.all()

Librarian_books = Librarian.objects.get(library=library_name)