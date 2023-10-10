from django.shortcuts import render
from django.http import HttpResponse
from . import util
from django import forms

import random
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entree(request, title):
    context = {
        'title': title,
        'entree': markdown2.markdown(util.get_entry(title)),
        'entries': util.list_entries(),
        'check': title in util.list_entries()
    }

    return render(request, 'encyclopedia/entree.html', context)

def search(request):

    if request.method == 'POST':
        form_data = request.POST
        title = form_data['q']
        if title in util.list_entries():
            context={
                'title': title,
                'entree': util.get_entry(title),
                'entries': util.list_entries(),
                'check': title in util.list_entries()
            }

            return render(request, 'encyclopedia/entree.html', context)
        else:
            search_results = []
            for entry in util.list_entries():
                if title.lower() in entry.lower():
                    search_results.append(entry)

            context={
                'title': 'Search Results',
                'entries': search_results,
            }

            return render(request, 'encyclopedia/search_results.html', context)
        
class New_page(forms.Form):
    title = forms.CharField()
    textarea = forms.CharField(widget=forms.Textarea)

class EditPage(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea)

def new_page(request):
    if request.method == 'POST':
        data = New_page(request.POST)
        if data.is_valid():
            title = data.cleaned_data.get('title')
            content = data.cleaned_data.get('textarea')

            for entry in util.list_entries():
                if title.lower() == entry.lower():
                    data = 'Title Exists already!!. pls choose another Title.'
                    return render(request, 'encyclopedia/ERROR.html', {'data': data})
                else:
                    util.save_entry(title, content)
                    context = {
                    'title': title,
                    'entree': util.get_entry(title),
                    'entries': util.list_entries(),
                    'check': title in util.list_entries()
                    }

                    return render(request, 'encyclopedia/entree.html', context)
                        
    return render(request, 'encyclopedia/new_page.html', {
        'form': New_page()
    })

def edit_page(request, title):
    content = util.get_entry(title)
    if request.method == 'POST':
        data = EditPage(request.POST)
        if data.is_valid():
            content = data.cleaned_data.get('textarea')
            util.save_entry(title, content)
            context = {
            'title': title,
            'entree': markdown2.markdown(util.get_entry(title)),
            'entries': util.list_entries(),
            'check': title in util.list_entries()
            }

            return render(request, 'encyclopedia/entree.html', context)

    return render(request, 'encyclopedia/EditPage.html', {
        'form': EditPage(initial={'textarea': content}),
        'title': title
    })


def randomPage(request):
    title = random.choice(util.list_entries())
    context = {
        'title': title,
        'entree': markdown2.markdown(util.get_entry(title)),
        'entries': util.list_entries(),
        'check': title in util.list_entries()
    }

    return render(request, 'encyclopedia/entree.html', context)
