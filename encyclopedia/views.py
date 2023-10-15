from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2
from . import util

markdowner = markdown2.Markdown()
entry_list = util.list_entries()

class Form(forms.Form):
    textarea = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder": "Enter the markdown content here..."}))
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Title..."}))
    

# home page
def index(request):
    if request.method == "POST":
        search = request.POST.get("q")
        match_list = []
        for entry in entry_list:
            if search.lower() == entry.lower():
                return HttpResponseRedirect(f"wiki/{entry}")
            elif str(search).lower() in entry.lower():
                match_list.append(entry)

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

# Create new page
def new_page(request):
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]
            
            if title.lower() in [entry.lower() for entry in entry_list]:
                return render(request, "encyclopedia/new.html", {"form": None})

            util.save_entry(title, content)
            return redirect(reverse("wiki", args=[title]))
        else:
            return render(request, "encyclopedia/new.html", {"form": form})
    return render(request, "encyclopedia/new.html", {"form": Form()})