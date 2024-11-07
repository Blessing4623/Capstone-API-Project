# Adding a  new title
go_book = Book.objects.get(title="1984")
go_book.title= "Nineteen Eighty-Four"
go_book.save()

# Expected output: {'id': 1, 'title': 'Nineteen Eighty-Four', 'author': 'George Orwell', 'publication_year': 1949}