from django.urls import include, path
from django.contrib.auth import views as auth_views
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'book', BookViewSet)

urlpatterns =[
    path('', home,name='home'),
    path('', include(router.urls)),
    path('managebooks/', manage_books,name='managebooks'),
    path('importbooks/', import_books,name='importbooks'),
    path('rest/', rest_api, name='rest_api'),
]