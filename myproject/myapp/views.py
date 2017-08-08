# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            newdoc = Document(docfile=request.FILES['docfile_2'])
            newdoc.save()

            # Redirect to the document list after POST
            # return HttpResponseRedirect(reverse('list'))
            return HttpResponseRedirect('/myapp/uploads/')
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    documents = documents[len(documents) - 2:]

    # Render list page with the documents and the form
    return render(request, 'list.html', {
        'documents': documents, 
        'form': form
        }
    )

def index(request):
    return render(request, 'index.html')


def uploads(request):
     # Load documents for the list page
    documents = Document.objects.all()
    documents = documents[len(documents) - 2:]
    return render(request, 'uploads.html', {'documents': documents})

def custom(request):
    return render(request, 'custom_input.html')