from django.test import TestCase

from ..forms import CreateBookForm


class CreateBookFormTest(TestCase):
    def test_valid_form(self):
        form = CreateBookForm(
            data={
                "title": "title",
                "author": "author",
                "published_date": 966,
                "isbn": "test",
                "pages": 123,
                "cover_picture": "test",
                "language": "pl",
            }
        )
        self.assertTrue(form.is_valid())

    def test_missing_field_form(self):
        form = CreateBookForm(
            data={
                "title": "title",
                "author": "author",
                "published_date": 966,
                "isbn": "test",
                "pages": 123,
            }
        )
        self.assertFalse(form.is_valid())

    def test_inavlid_type_form(self):
        form = CreateBookForm(
            data={
                "title": "title",
                "author": "author",
                "published_date": "test",
                "isbn": "test",
                "pages": "test",
                "cover_picture": "test",
                "language": "pl",
            }
        )
        self.assertFalse(form.is_valid())
