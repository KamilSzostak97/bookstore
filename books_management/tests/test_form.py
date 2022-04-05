from django.test import TestCase

from ..forms import createbookform


class CreateBookFormTest(TestCase):
    def valid_form_test(self):
        form = createbookform(
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

    def missing_field_form_test(self):
        form = createbookform(
            data={
                "title": "title",
                "author": "author",
                "published_date": 966,
                "isbn": "test",
                "pages": 123,
            }
        )
        self.assertFalse(form.is_valid())

    def inavlid_type_form_test(self):
        form = createbookform(
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
