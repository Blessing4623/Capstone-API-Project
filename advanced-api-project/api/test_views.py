from django.test import TestCase
from .models import Book
class BookTest(TestCase):
    def setUp(self):
        self.book_data = {
            'title' : 'One way',
            'publication_year': 2014,
            'author': 'Rose'
        }
    def test_create_book(self):
        response = self.client.Post(self.list_create_url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.book_data['title'])
    def test_read_book(self):
        response = self.client.Get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    