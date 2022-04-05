from django.test import TestCase

from ..models import Book


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Book.objects.create(
            title="test",
            author="case",
            published_date=966,
            isbn="123",
            pages=10,
            cover_picture="none",
            language="pl",
        )

    def test_title_label(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.title, "test")
        self.assertEqual(book.author, "case")
        self.assertEqual(book.published_date, 966)
        self.assertEqual(book.isbn, "123")
        self.assertEqual(book.pages, 10)
        self.assertEqual(book.cover_picture, "none")
        self.assertEqual(book.language, "pl")

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field("title").max_length
        self.assertEqual(max_length, 200)
