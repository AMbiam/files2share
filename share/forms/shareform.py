from django import forms
from django.core.exceptions import ValidationError

# Validators
# https://docs.djangoproject.com/en/5.2/ref/validators/#validate-email
class ShareRetrievalForm(forms.Form):
    print("Valid form submission....")
    addr = forms.EmailField(
        label = 'E - mail',
        max_length = 30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-5',
                'placeholder': 'E - Mail',
                'aria-label': 'e mail',
            }
        ),
    )

    fileid = forms.CharField(
        label= 'File Identifier',
        max_length = 40,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-5',
            'placeholder': 'File ID',
            'aria-label': 'file ID',
        }),
    )

    passcode = forms.CharField(
        label= 'Access Code',
        max_length = 40,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-5',
            'placeholder': 'Search',
            'aria-label': 'Search',
        }),
    )


