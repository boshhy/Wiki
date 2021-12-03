import re
import random
from typing import ContextManager, Type
from django import http
from django.forms.fields import TypedMultipleChoiceField
from django.forms.widgets import Textarea
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from . import util
import markdown2
from django.contrib import messages


# Gets a list of all entries on our Wiki page and assigns the to "entries"
# Index.html generates a page with the list "entries"
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Given a name of an entry, look for it in the util.get_entry()
def entry(request, name):
    entry = util.get_entry(name)
    # If found, pass the name and its contents(with markdown applied) to entry.html
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": name.capitalize(),
            "entry": markdown2.markdown(entry)
        })
    # If not found generate the notFound.html
    else:
        return render(request, "encyclopedia/notFound.html", {
            "title": name
        })


# This searches and returns all substring matches for the user search
def search(request):
    if request.method == "GET":
        # Gets the search and entries and assigns them to variables
        the_search = request.GET.get("q")
        the_entries = util.list_entries()
        the_list = []

        # If an entry matches exactly return the Wiki page by going to entry.html and passing the search argument
        if util.get_entry(the_search):
            return HttpResponseRedirect(reverse("entry", args=[the_search]))

        # Look through entries for matching substring
        for entry in the_entries:
            if the_search.upper() in entry.upper():
                # If substring matches entry add entry to the_list
                the_list.append(entry)

        # If nothing was found return proper response
        if not the_list:
            return render(request, "encyclopedia/index.html", {
                "nothing_found": True
            })

        # Display the list of items with matching substring
        return render(request, "encyclopedia/index.html", {
            "nothing_found": False,
            "entries": the_list
        })
    else:
        return HttpResponse("An error occured")


# Blue print for form that will be used for editing and creating new entries
class NewTaskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Page Title", 'style': 'font-size: 24px'}))
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            "placeholder": "Page Content",
            'style': 'height: 300px; width: 90%', }))


# Logic for creating a new entry
def new_entry(request):
    if request.method == "POST":
        # Get the form contents submitted and assign object to 'form'
        form = NewTaskForm(request.POST)

        # Check to see if form is valid
        if form.is_valid():
            # Strip the 'title' and 'text' contents and assign to variables
            new_title = form.cleaned_data["title"]
            new_content = form.cleaned_data["text"]

            # If Wiki entry already exists, give the user a warning message and keep user contents for editing
            if util.get_entry(new_title):
                return render(request, "encyclopedia/new.html", {
                    "in_wiki": True,
                    "form": form
                })
            # Save new entry to Wiki and save it as bytes (this must be done so we don't get a new line error)
            # Redirect the user to the newly created page
            else:
                util.save_entry(new_title, bytes(new_content, 'utf8'))
                return HttpResponseRedirect(reverse("entry", args=[new_title]))
    # This will be returned if a user is requesting to create a new page. (blank form)
    else:
        return render(request, "encyclopedia/new.html", {
            "in_wiki": False,
            "form": NewTaskForm()
        })


# This will let a user edit an existing Wiki page
def edit(request, name):
    # If method is 'GET' then display a form with the exising content for current page
    if request.method == "GET":
        current_text = util.get_entry(name)
        initial_dict = {
            "title": name,
            "text": current_text,
        }
        # The below line initialized the form with content for the Wiki entry
        form = NewTaskForm(initial=initial_dict)
        # Display edit.html with contents prefilled with Wiki contents
        return render(request, "encyclopedia/edit.html", {
            "title": name,
            "form": form
        })
    # If methos is "POST" then user is submitting changes to current Wiki entry
    elif request.method == "POST":
        # Get form with updated data
        form = NewTaskForm(request.POST)

        if form.is_valid():
            # Strip the new "text" content and overide old contents with new
            new_content = form.cleaned_data["text"]
            util.save_entry(name, bytes(new_content, "utf8"))
            # Redirect the user to the new updated entry.html page
            return HttpResponseRedirect(reverse("entry", args=[name]))
    else:
        return HttpResponse("An error occured")


# Get a random title from entries and take user to entry.html associated with the random
def random_entry(request):
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", args=[entry]))
