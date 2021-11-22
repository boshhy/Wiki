from django.shortcuts import render
from django.http import HttpResponse  # might be able to delete this

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, name):
    if util.get_entry(name):
        return render(request, "encyclopedia/entry.html", {
            "title": name.capitalize(),
            # right now it doesnt format the page properly
            "entry": util.get_entry(name),
        })
    else:
        return HttpResponse("not in the system")
