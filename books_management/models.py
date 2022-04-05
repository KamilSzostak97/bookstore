from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=200, null=True)
    published_date = models.IntegerField()
    isbn = models.CharField(max_length=200, null=True)
    pages = models.IntegerField()
    cover_picture = models.CharField(max_length=900, null=True)
    language = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.title)
