from django import forms
from django.core.exceptions import ValidationError

from .models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        
        fields = ('title', 'filename', 'file')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-5'}),
            'filename': forms.TextInput(attrs={'class': 'form-control mb-5'}),
            'file': forms.FileInput(attrs={'class': 'form-control mb-5'}),
        }

        labels = {
            'title': 'What do you want to call this file.',
            'filename': 'File name',
            'upload': 'Upload File',
        }


class ShareRetrievalForm(forms.Form):
    email = forms.CharField(max_length = 200)
    fileid = forms.CharField(max_length = 200)
    passcode = forms.CharField(max_length = 200)