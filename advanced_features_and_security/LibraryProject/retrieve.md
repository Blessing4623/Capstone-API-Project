# Retrieving all the data from the model Book and its subsequent values
books = Book.objects.all().values()
for book in books:
     print(book)


# Expected output: {'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}