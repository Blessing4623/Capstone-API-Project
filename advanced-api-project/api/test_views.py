from django.test import TestCase
from .models import Book, Author
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
class BookTest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Rose')
        self.client.login(username='user', password='1234')
        self.book_data = {
            'title' : 'One way',
            'publication_year': 2014,
            'author': self.author
        }
        self.book = Book.objects.create(**self.book_data)
        self.list_create_url = reverse('book_create')
    def test_create_book(self):
        response = self.client.Post(self.list_create_url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.book_data['title'])
    def test_read_book(self):
        response = self.client.Get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_update_book(self):
        update_data = ['title' == 'Two Ways']
        url = reverse('book_detail', kwargs={'pk': self.book.pk})
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book.title, 'Two Ways')
    def test_delete_book(self):
        url = reverse('book_detail', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)