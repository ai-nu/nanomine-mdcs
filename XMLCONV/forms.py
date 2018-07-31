from django import forms
from .models import *

class DocumentForm(forms.Form):
    templatefile = forms.FileField(
        label='Select the template Excel file',
        widget = forms.ClearableFileInput(attrs={'multiple':False, 'required':True})
    )
    docfile = forms.FileField(
        label='Select all other files',
        widget = forms.ClearableFileInput(attrs={'multiple':True}),
        required = False
    )

