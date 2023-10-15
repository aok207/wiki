from django.shortcuts import render
import markdown2
from . import util

markdowner = markdown2.Markdown()

# home page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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

    return render(request, "encyclopedia/wiki.html", {"page": page_name.upper(), "content": content})