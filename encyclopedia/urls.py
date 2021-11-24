from hashlib import new
from os import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new_entry, name="new_entry"),
    path("edit/<str:name>/", views.edit, name="edit")
]
