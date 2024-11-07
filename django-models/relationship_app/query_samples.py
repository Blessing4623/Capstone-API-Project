from .models import Book, Author, Library, Librarian

author = Author.objects.get(name=author_name)
books_by_author= Book.objects.filter(author=author)
library = Library.objects.get(name=library_name)
library.books.all()

Librarian_books = Librarian.objects.get(library=library_name)