import re
from django import http
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse  # might be able to delete this
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, name):
    entry = util.get_entry(name)
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": name.capitalize(),
            # right now it doesnt format the page properly
            "entry": markdown2.markdown(entry)
        })
    else:
        return HttpResponse("not in the system")


def search(request):
    if request.method == "GET":
        the_search = request.GET.get("q")
        the_entries = util.list_entries()
        the_list = []

        if util.get_entry(the_search):
            return HttpResponseRedirect(reverse("entry", args=[the_search]))

        # look through entries for matching substring
        for entry in the_entries:
            if the_search.upper() in entry.upper():
                # if substring matches entry add entry to the_list
                the_list.append(entry)

        # if nothing was found return proper response
        if not the_list:
            return HttpResponse("nothing found")

        # display the list of items with matching substring
        return render(request, "encyclopedia/index.html", {
            "entries": the_list
        })
    else:
        return HttpResponse("an error occured")
