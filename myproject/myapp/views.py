# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm

from collections import OrderedDict

from image_utils import ImageText
from PIL import Image

from tasks import add
from tasks import tax
from tasks import merge

import ffmpy
import os


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            #uploads img
            img = Document(docfile=request.FILES['docfile'])
            img.save()

            #uploads audio
            audio = Document(docfile=request.FILES['docfile_2'])
            audio.save()


            # dir_path = os.path.dirname(os.path.realpath(__file__))
            # cwd = os.getcwd()

            #gets name of audio file without the extension
            audioBase = os.path.splitext(os.path.basename(audio.docfile.name))[0] 

            #new file destination with .mp4 extension
            newFile = '/media/output/' + audioBase + '.mp4'

            print '************************************'
            print img.docfile.url
            resize = Image.open('.' + img.docfile.url)
            size = resize.size
            if size != (1280,720):
                if size[0] > size[1]:
                    resize = resize.resize((1280, size[1]*1280/size[0]))
                else:
                    resize = resize.resize((size[0]*720/size[1], 720))
                size = resize.size
                x = (1280 - size[0]) / 2
                y = (720 - size[1]) / 2
                canvas = Image.new('RGB', (1280, 720), (0,0,0))
                canvas.paste(resize, (x,y), resize)
                canvas.save('.' + img.docfile.url)


            # ff = ffmpy.FFmpeg(
            #     global_options='-loop 1',
            #     inputs=OrderedDict([('./media/' + img.docfile.name, None), ('./media/' + audio.docfile.name, None)]),
            #                         # {
            #                         #     './media/' + img.docfile.name: None,
            #                         #     './media/' + audio.docfile.name: None
            #                         # },



            #                         # outputs={'../../media/files/' + audio.docfile.name + '.mp4': '-c:v libx264 -c:a aac -shortest'}
            #                         # outputs={'./media/output/test_result.mp4': '-c:v libx264 -c:a aac -shortest'}
            #     outputs={'.' + newFile: '-c:v libx264 -c:a aac -shortest'}
            # )

            # print ff.cmd

            # ff.run()

            merge.delay('./media/' + img.docfile.name, './media/' + audio.docfile.name, '.' + newFile)

            request.session['newFile'] = newFile
            request.session['newFileName'] = audioBase + '.mp4'

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
    # documents = Document.objects.all()
    # documents = documents[len(documents) - 2:]
    # print '*********************************'
    # print request.session['newFile']
    # return render(request, 'uploads.html', {'documents': documents, })


    return render(request, 'uploads.html', {'newFile': request.session['newFile'], 'name': request.session['newFileName']})

def custom(request):
    if request.method == 'POST':
        bgcolor = (0,0,0)
        if request.POST['color'] == 'color2':
            bgcolor = (255,0,0, 255)
        elif request.POST['color'] == 'color3':
            bgcolor = (0,255,0, 255)
        elif request.POST['color'] == 'color4':
            bgcolor = (0,0,255, 255)
       


        color =  (255,255,255)
        text = request.POST['text']
        font = 'arial.ttf'
        img = ImageText((1280, 720), background=bgcolor)

        img.write_text_box((200, 200), text, box_width=880, font_filename=font, font_size=24, color=color, place='center')

        audio = Document(docfile = request.FILES['audio'])
        audio.save()

        audioBase = os.path.splitext(os.path.basename(audio.docfile.name))[0] 
        newFile = '/media/output/' + audioBase + '.mp4'

        img.save('./media/input/' + audioBase + '_img.png')

        # ff = ffmpy.FFmpeg(
        #     global_options='-loop 1',
        #     inputs=OrderedDict([('./media/input/' + audioBase + '_img.png', None), ('./media/' + audio.docfile.name, None)]),
        #     outputs={'.' + newFile: '-c:v libx264 -c:a aac -shortest'}
        # )

        # ff.run()

        merge.delay('./media/input/' + audioBase + '_img.png', './media/' + audio.docfile.name, '.' + newFile)

        request.session['newFile'] = newFile
        request.session['newFileName'] = audioBase + '.mp4'


        return HttpResponseRedirect('/myapp/uploads/')

    else:
        # tax.delay()
        # tax.delay()
        # add.delay(7,8)
        # add.delay(7,8)
        # merge.delay('python1.png', 'custom.wav', 'output.mp4')
        # add.delay(7,8)
        # add.delay(7,8)
        return render(request, 'custom_input.html')