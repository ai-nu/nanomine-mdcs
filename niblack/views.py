from django.shortcuts import render_to_response, render, RequestContext, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from niblack.models import Document
from niblack.forms import *

import xmltodict
import os
import scipy.io
# Create your views here.

def home(request):
	if request.user.is_authenticated():
	    # Handle file upload
	    if request.method == 'POST':
			form = DocumentForm(request.POST, request.FILES)
			if form.is_valid():
				newdoc = Document(docfile = request.FILES['docfile'])
				newdoc.save()
				file = request.FILES['docfile'] #get name of incoming file
				# Initialize adjust value and window size
				f = open('./niblack/mfiles/adjust.txt', 'w')
				s = str('0')
				f.write(s)
				f.close()
				f = open('./niblack/mfiles/winsize', 'w')
				w = str('5')
				f.write(w)
				f.close()
				if not str(file).endswith(".jpg"):
					if not str(file).endswith(".JPG"):
							if not str(file).endswith(".tif"):
								if not str(file).endswith(".png"):
									if not str(file).endswith(".PNG"):
										if not str(file).endswith(".TIF"):
											return HttpResponse('<h3>Please upload an image in supported format (.jpg, .png or .tif)</h3>') #report wrong file format				
				# Run MATLAB when file is valid
				os.system('matlab -nodesktop -nodisplay -nojvm -nosplash -r "cd niblack/mfiles;run_niblack(\'"'+str(file)+'"\');exit"')
				os.system('mv ./niblack/media/documents/jpg/NBbefore.jpg /var/www/html/nm/Binarization/Niblack/NBbefore.jpg')
				os.system('mv ./niblack/media/documents/jpg/NBafter.jpg /var/www/html/nm/Binarization/Niblack/NBafter.jpg')
				
				# Redirect to the document list after POST
				return HttpResponseRedirect(reverse('niblack.views.check'))
			else:
				return HttpResponse('<h3>Please upload an image!</h3>') # if no image was uploaded, report error
	    else:
			form = DocumentForm() # A empty, unbound form

			# Load documents for the list page
			documents = Document.objects.all()
			  
			# Render list page with the documents and the form
			return render_to_response('niblack.html',{'documents': documents, 'form': form},context_instance=RequestContext(request))
	else:
		return redirect('/login')

def check(request):
	if request.user.is_authenticated():
	    # Perform dynamic binarization
	    
	    # Load summary parameters
	    if os.path.isfile('./niblack/mfiles/niblack/imgs/NiblackSummary.mat'):
		mat = scipy.io.loadmat('./niblack/mfiles/niblack/imgs/NiblackSummary.mat')
		fname = (mat['fname'][0])
		img_size = int(mat['img_size'])
		win_size = int(mat['win_size']) # adjusted window size
		VF = float(mat['VF']) # volume fraction of white phase
	    else:
		fname = ''
		img_size = ''
		win_size = ''
	    
	    # Get adjust win size value from form
	    if request.method == 'POST':
			form = NiblackAdjustForm(request.POST)
			if form.is_valid():
				adjust = request.POST['adjust']
				#adjust = NiblackAdjust(AdjustValue)
				print 'User input adjust win size:'
				print request.POST['adjust']
				
				f1 = open('./niblack/mfiles/adjust.txt', 'w')
				s = str(adjust)
				f1.write(s)
				f1.close()
				
				f2 = open('./niblack/mfiles/winsize', 'w')
				s2 = str(win_size)
				print s2
				f2.write(s2)
				f2.close()
				
				# Run MATLAB when form is valid
				os.system('matlab -nodesktop -nodisplay -nojvm -nosplash -r "cd niblack/mfiles;run_niblack(\'"'+str(fname)+'"\');exit"')
				os.system('mv ./niblack/media/documents/jpg/NBbefore.tif /var/www/html/nm/Binarization/Niblack/NBbefore.tif')
				os.system('mv ./niblack/media/documents/jpg/NBafter.jpg /var/www/html/nm/Binarization/Niblack/NBafter.jpg')
				#Update window size and volume fraction
				if os.path.isfile('./niblack/mfiles/niblack/imgs/NiblackSummary.mat'):
					mat = scipy.io.loadmat('./niblack/mfiles/niblack/imgs/NiblackSummary.mat')
					win_size = int(mat['win_size']) # adjusted window size
					VF = float(mat['VF']) # volume fraction of white phase
				else:
					win_size = ''
                                return render_to_response('niblack_result.html',{'fname':fname, 'win_size': win_size, 'volume_fraction':VF, 'form':form},context_instance=RequestContext(request))
          
	    else:
			form = NiblackAdjustForm()
			return render_to_response('niblack_result.html',{'fname':fname, 'win_size': win_size, 'volume_fraction':VF, 'form':form},context_instance=RequestContext(request))
	else:
		return redirect('/login')
