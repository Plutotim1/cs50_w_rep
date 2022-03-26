from django.shortcuts import render, HttpResponse, redirect
from django import forms
from markdown2 import Markdown
from . import util
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def show_entry(request, entry):
    marker = Markdown()
    if (entry_to_show := util.get_entry(entry)) == None:
        return HttpResponse("ERROR \n Entry not found")
    markdown = marker.convert(entry_to_show)
    return render(request, "encyclopedia/entry.html",{"mark": markdown, "entry": entry})
    return HttpResponse(markdown)


def random(request):
    entry = choice(util.list_entries())
    if entry != None:
        return redirect(f"wiki/{entry}")
    return HttpResponse("Error: No entrys exist")

def add(request, content="Example:\n #CSS\nCSS is a language that can be used to add style to an [HTML](/wiki/HTML) page."):
    class Editor(forms.Form):
        title = forms.CharField()
        contents = forms.CharField(widget= forms.Textarea, initial=content)
    if request.method == "GET":
        return render(request, "encyclopedia/add.html", {"form": Editor()})
    elif request.method == "POST":
        form = Editor(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["contents"]
            title = form.cleaned_data["title"]
            if util.get_entry(title) != None:
                return render(request, "encyclopedia/error.html", {"message": "Title already exists"})
            util.save_entry(title, entry)
            return redirect(f"wiki/{title}")
        return redirect("index")


def edit_entry(request, entry_name):
    class Editor(forms.Form):
        name_of_entry = forms.CharField(widget = forms.HiddenInput, initial= entry_name)
        contents = forms.CharField(widget= forms.Textarea, initial=util.get_entry(entry_name))
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {"form": Editor(), "entry_name": entry_name})
    elif request.method == "POST":
        form = Editor(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["contents"]
            entry_name = form.cleaned_data["name_of_entry"]
            util.save_entry(entry_name, entry)
            return redirect(f"/wiki/{entry_name}")
def search(request):
    searched_for = request.GET.get("q")
    if (entry := util.get_entry(searched_for)) == None:
        incl_entrys = []
        for entry_title in util.list_entries():
            if searched_for in entry_title:
                incl_entrys.append(entry_title)
        return render(request, "encyclopedia/search_entrys.html", {"entrys": incl_entrys})
                
    return redirect(f"/wiki/{searched_for}")




