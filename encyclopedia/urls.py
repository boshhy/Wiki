from hashlib import new
from os import name
from django.urls import path

from . import views

# Holds all the paths for url inputs, along with the function that should be called
# and a 'nickname' for each path
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new_entry, name="new_entry"),
    path("edit/<str:name>/", views.edit, name="edit"),
    path("random/", views.random_entry, name="random"),
]
