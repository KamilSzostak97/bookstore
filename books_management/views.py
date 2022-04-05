"""
views.py includes backend for boostore application
"""
import json
from email import message

import requests
from django.shortcuts import redirect, render
from numpy import delete
from rest_framework import viewsets

from bookstore.settings import GOOGLE_API_KEY

from .forms import CreateBookForm
from .models import Book
from .serializers import BookSerializer

GOOGLE_API_URL = "https://www.googleapis.com/books/v1/volumes?q="

# Create your views here.
def home(request):
    """Homepage contains list of all books in database"""
    if "filterby" in request.GET:
        filter_category = request.GET["filterby"]

    if "search" in request.GET:
        if (
            request.GET["date_search"] is not None
            and request.GET["date_search"].isnumeric()
        ):
            books = Book.objects.filter(
                published_date__gte=request.GET["search"]
            ).filter(published_date__lte=request.GET["date_search"])
        else:
            dynamic_filter = {}
            dynamic_filter[filter_category] = request.GET["search"]
            books = Book.objects.filter(**dynamic_filter)
    else:
        books = Book.objects.all()

    context = {"books": books}
    return render(request, "book/home.html", context)


def manage_books(request):
    """Add and edit books"""
    message = []
    form = CreateBookForm()
    if "isbn_search" in request.GET:
        message = ["Leave blank to select first entry in database"]
        requested_isbn = request.GET["isbn_search"]

        instance = Book.objects.filter(isbn__icontains=requested_isbn).first()

        if instance is None:
            message = ["Inputed ISBN doesn't match any entry"]
            return render(
                request, "book/managebooks.html", {"form": form, "messages": message}
            )

        if request.GET["option_select"] == "delete":
            instance.delete()
            return redirect("/")

        form = CreateBookForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        if request.method == "POST":
            form = CreateBookForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("/")
    return render(request, "book/managebooks.html", {"form": form, "messages": message})


def import_books(request):
    """Import books from Google Books API"""
    if "filterby" in request.GET:
        filter_category = request.GET["filterby"]

    if "import" in request.GET:
        search = request.GET["import"]
        if search == "":
            return redirect("importbooks")

        response_api = requests.get(
            f"{GOOGLE_API_URL}{filter_category}:{search}&printType=books&key={GOOGLE_API_KEY}"
        )

        data = response_api.text
        parse_json = json.loads(data)

        if not parse_json["totalItems"]:
            return render(request, "book/importbooks.html")

        for book_index in range(len(parse_json["items"])):
            model = Book()
            if "title" in parse_json["items"][book_index]["volumeInfo"]:
                model.title = parse_json["items"][book_index]["volumeInfo"]["title"]
            else:
                model.pages = "No information available"

            if "authors" in parse_json["items"][book_index]["volumeInfo"]:
                authors = []
                for author_index in range(
                    len(parse_json["items"][book_index]["volumeInfo"]["authors"])
                ):
                    authors.append(
                        parse_json["items"][book_index]["volumeInfo"]["authors"][
                            author_index
                        ]
                    )

                model.author = ", ".join(authors)
            else:
                model.author = "No information available"

            if "publishedDate" in parse_json["items"][book_index]["volumeInfo"]:
                date = parse_json["items"][book_index]["volumeInfo"]["publishedDate"]
                model.published_date = int(date[0:4])
            else:
                model.published_date = 0

            if "industryIdentifiers" in parse_json["items"][book_index]["volumeInfo"]:
                isbn = []
                for isbn_index in range(
                    len(
                        parse_json["items"][book_index]["volumeInfo"][
                            "industryIdentifiers"
                        ]
                    )
                ):
                    isbn.append(
                        parse_json["items"][book_index]["volumeInfo"][
                            "industryIdentifiers"
                        ][isbn_index]["identifier"]
                    )

                model.isbn = ", ".join(isbn)
            else:
                model.pages = "No information available"

            if "pageCount" in parse_json["items"][book_index]["volumeInfo"]:
                model.pages = parse_json["items"][book_index]["volumeInfo"]["pageCount"]
            else:
                model.pages = 0

            if "imageLinks" in parse_json["items"][book_index]["volumeInfo"]:
                model.cover_picture = parse_json["items"][book_index]["volumeInfo"][
                    "imageLinks"
                ]["thumbnail"]
            else:
                model.cover_picture = "No information available"

            model.language = parse_json["items"][book_index]["volumeInfo"]["language"]
            model.save()
        return redirect("/")
    return render(request, "book/importbooks.html")


def rest_api(request):
    """Backend for rest api searchbar"""
    if "filterby" in request.GET:
        filter_category = request.GET["filterby"]

    if "search" in request.GET:
        search_value = request.GET["search"]
        return redirect(
            f"/book/?search={search_value}&filterby={filter_category}&format=json"
        )
    return render(request, "book/rest.html")


class BookViewSet(viewsets.ModelViewSet):
    """Rest api and querryset"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Filter returned books
        """
        queryset = Book.objects.all()
        search = self.request.query_params.get("search")
        filterby = self.request.query_params.get("filterby")
        dynamic_filter = {}
        dynamic_filter[filterby + "__icontains"] = search
        if search is not None and filterby is not None:
            queryset = queryset.filter(**dynamic_filter)
        return queryset
