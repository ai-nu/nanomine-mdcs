from django import forms

Input_types = (
	      (1,('Single image')),
	      (3,('Single Image in .mat format')),
	      (2,('ZIP File containing multiple images')),)

class DocumentForm(forms.Form):
	docfile = forms.FileField(
		label ='Select File'
	)
	email_id = forms.EmailField(
		 label='Enter Email address to receive Job ID:',required=False
	)
	input_type = forms.ChoiceField(
		label='Select Input Option',choices=Input_types,required=False,initial=''
	)

