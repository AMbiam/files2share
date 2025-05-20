from django import forms
from django.core.exceptions import ValidationError

from share.models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        
        fields = ('icon','title', 'filename', 'file')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-5'}),
            'filename': forms.TextInput(attrs={'class': 'form-control mb-5'}),
            'file': forms.FileInput(attrs={'class': 'form-control mb-5'}),
            'icon': forms.FileInput(attrs={'class': 'form-control mb-5'}),
        }

        labels = {
            'icon': 'File Icon',
            'title': 'What do you want to call this file.',
            'filename': 'File name',
            'upload': 'Upload File',
        }
