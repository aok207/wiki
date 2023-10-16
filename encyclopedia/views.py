from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2
from random import choice
from . import util

markdowner = markdown2.Markdown()
# This variable is used in edit function to store the entry page title that user want to edit.
final_entry_page = None

# Form for "create new page"
class Form(forms.Form):
    textarea = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder": "Enter the markdown content here..."}))
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Title..."}))

# Form for "edit page"
class Edit_form(forms.Form):
    textarea = forms.CharField(label="", widget=forms.Textarea)    

# home page
def index(request):
    if request.method == "POST":
        # Implanting Search feature #
        search = request.POST.get("q")
        entry_list = util.list_entries()
        match_list = []
        if len(search) > 0:
            # Loop through the list of entry
            for entry in entry_list:
                # If there's a match, redirect to that matched page
                if search.lower() == entry.lower():
                    return HttpResponseRedirect(f"wiki/{entry}")
                # If a substring is matched, add it to the match_list
                elif search.lower() in entry.lower():
                    match_list.append(entry)
            
            return render(request, "encyclopedia/index.html", {
                "entries": match_list, 
                "title": f"Searches results for '{search}'"
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(), "title": "All Pages"
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

    return render(request, "encyclopedia/wiki.html", {"page": page_name.capitalize(), "content": content, "page_name": page_name})

# Create new page
def new_page(request):
    if request.method == "POST":
        form = Form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]
            entry_list = util.list_entries()
            
            # If title already exists, throw an error, by passing in None as "form" value.
            if title.lower() in [entry.lower() for entry in entry_list]:
                return render(request, "encyclopedia/new.html", {"form": None})

            util.save_entry(title, content)
            return redirect(reverse("wiki", args=[title]))
        else:
            return render(request, "encyclopedia/new.html", {"form": form})
    return render(request, "encyclopedia/new.html", {"form": Form()})

# Edit page
def edit(request):
    global final_entry_page
    # This variable stores the name of the entry page user want to edit
    # The value is pass in as a hidden value when the user click the edit button.
    entry_page = request.GET.get("page_name")
    
    entry_data = Edit_form(initial={"textarea": util.get_entry(entry_page)})
    # If the user get to this page via post
    if request.method == "POST":
        # Get the form
        form = Edit_form(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Get the content and save the file
            content = form.cleaned_data["textarea"]
            util.save_entry(final_entry_page, content)

            # Redirect the user to that updated entry page
            return redirect(reverse("wiki", args=[final_entry_page]))
        # If form not valid
        else:
            # Hand them back the form and not save anything    
            return render(request, "encyclopedia/edit.html", {"page_name": final_entry_page, "form": form})
    # If the user get to this page via get
    else:
        if entry_page is not None:
            final_entry_page = entry_page    
            return render(request, "encyclopedia/edit.html", {"page_name": entry_page, "form": entry_data})
        else:
            return redirect(reverse("index"))

# Random function       
def random(request):
    return redirect(reverse("wiki", args=[choice(util.list_entries())]))