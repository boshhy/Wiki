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
