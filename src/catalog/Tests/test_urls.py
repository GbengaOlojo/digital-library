'''
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from catalog.views import index, Book_detail_view, author_list_views, author_detail_view, rent_book, return_book


class TestUrls(SimpleTestCase):


    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)


    def test_book_detailed_view_url_is_resolved(self):
        url = reverse('book_detailed_view')
        self.assertEquals(resolve(url).func, book-detail)

    def test_author_list_views_url_is_resolved(self):
        url = reverse('author_list_views')
        self.assertEquals(resolve(url).func, index)

    def test_author_detail_view_url_is_resolved(self):
        url = reverse('author_detail_view')
        self.assertEquals(resolve(url).func, author_detail_view)


    def test_rent_book_url_is_resolved(self):
        url = reverse('rent_book')
        self.assertEquals(resolve(url).func, rent_book)

    def test_return_book_url_is_resolved(self):
        url = reverse('return_book')
        self.assertEquals(resolve(url).func, return-book)
'''