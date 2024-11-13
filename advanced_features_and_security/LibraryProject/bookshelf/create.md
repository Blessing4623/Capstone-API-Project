# Creating a new Book instance and saving it
from bookshelf.models import Book
new_book = Book.objects.create(title="1984", author="George Orwell", publication_year="1949")       
new_book.save()

# Expected output: {'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}