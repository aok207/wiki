from django.shortcuts import render

from . import util

# home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# entry page
def wiki_page(request, page_name):
    return render(request, "encyclopedia/wiki.html", {"page": page_name.upper()})