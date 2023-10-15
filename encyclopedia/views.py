from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from . import util

markdowner = markdown2.Markdown()

# home page
def index(request):
    if request.method == "POST":
        search = request.POST.get("q")
        match_list = []
        for entry in util.list_entries():
            if search.lower() == entry.lower():
                return HttpResponseRedirect(f"wiki/{entry}")
            elif str(search).lower() in entry.lower():
                match_list.append(entry)

        print(match_list)
        return render(request, "encyclopedia/index.html", {
            "entries": match_list, 
            "title": f"Searches results for '{search}'"
        })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "title": "All Pages"
    })

# entry page
def wiki_page(request, page_name):
    # Get the content of the page using get entry function
    page_content = util.get_entry(page_name)
    # If the content is None, this will return None
    if page_content is None:
        content = None
    # Else convert it into HTML, and return that instead
    else:
        content = markdowner.convert(page_content)

    return render(request, "encyclopedia/wiki.html", {"page": page_name.capitalize(), "content": content})