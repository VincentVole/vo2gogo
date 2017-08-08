# -*- coding: utf-8 -*-

from django import forms


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select an image'
    )

    docfile_2 = forms.FileField(
        label='Select an audio clip'
    )