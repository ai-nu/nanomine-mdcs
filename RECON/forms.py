from django import forms

Input_types = (
	      (1,('Single image')),
	      (3,('Single Image in .mat format')),)

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
	num_recon = forms.IntegerField(
		 label='Enter number of reconstruction',required=False,initial=1,min_value=1,max_value=1
	)
