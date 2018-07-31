from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select file'
    )
    
class NiblackAdjustForm(forms.Form):
    adjust = forms.IntegerField(label='Enter Window Size (in pixels):', required=False,initial=5,min_value=1)    