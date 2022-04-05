from django.test import TestCase
from rest_framework.test import APIClient

from ..models import Book


class BookListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        books = 7

        for book in range(books):
            Book.objects.create(
                title="test",
                author="case",
                published_date=966,
                isbn="123",
                pages=10,
                cover_picture="none",
                language="pl",
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
