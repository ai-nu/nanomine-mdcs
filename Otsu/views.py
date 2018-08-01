from django.shortcuts import render_to_response, render, RequestContext, redirect
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from time import gmtime, strftime, localtime

from django.template import Context
from contextlib import contextmanager


from Otsu.models import Document
from Otsu.forms import *

import xmltodict
import os
import subprocess
import scipy.io
# Create your views here.

def Binarization_Choice(request):
        #if request.user.is_authenticated():
	       form = DocumentForm()
               documents = Document.objects.all()
               return render_to_response('Binarization_Choice.html',{'documents': documents, 'form': form},context_instance=RequestContext(request))
        #else:
               #return redirect('/login')

def checkResult(request):
	if request.user.is_authenticated():
		form = DocumentForm()
		documents = Document.objects.all()
		return render_to_response('Otsu_Check_Result.html',{'documents': documents, 'form': form},context_instance=RequestContext(request))
	else:
		return redirect('/login')

def viewResult(request):
	if request.user.is_authenticated():
		form = DocumentForm()
		documents = Document.objects.all()
		return render_to_response('Otsu_view_Result.html',{'documents': documents, 'form': form},context_instance=RequestContext(request))
	else:
		return redirect('/login')

def submission_notify(request):
	if request.user.is_authenticated():
		form = DocumentForm()
		documents = Document.objects.all()
		return render_to_response('Submission_notify.html',{'documents': documents, 'form': form},context_instance=RequestContext(request))
	else:
		return redirect('/login')

def Binarize_Otsu(request):
	if request.user.is_authenticated():
	  if request.method == "POST":
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
		    newdoc = Document(docfile = request.FILES['docfile'])
		    newdoc.save()

		    user_email_id = request.POST['email_id']
		    if not user_email_id:  # if no email provided, report error
				return HttpResponse('<h3>Please provide an email address to receive Job ID!</h3>')
		    work_dir = '/home/NANOMINE/Develop/mdcs'
		    os.chdir(work_dir)
		    os.system('pwd')
		    file = request.FILES['docfile'] #get name of incoming file
		    print type(str(file))
		    input_type = request.POST['input_type']
		    if input_type == "1":
					if not str(file).endswith(".jpg"):
						if not str(file).endswith(".JPG"):
							if not str(file).endswith(".tif"):
								if not str(file).endswith(".png"):
									if not str(file).endswith(".PNG"):
										if not str(file).endswith(".TIF"):
											return HttpResponse('<h3>Please upload a JPEG file</h3>') #report wrong file format
                    elif input_type == "2":
                        if not str(file).endswith(".zip"):
                          return HttpResponse('<h3>Please upload ZIP  file</h3>') #report wrong file format                 
                    else:
                        if not str(file).endswith(".mat"):
                          return HttpResponse('<h3>Please upload .mat file</h3>') #report wrong file format

		    user_name = None
		    user_name = request.user.get_username()
		    print (user_name)
		    # Run MATLAB when file is valid
		    os.system('matlab -nodesktop -nodisplay -nosplash -r "cd /home/NANOMINE/Production/mdcs/Otsu/mfiles;Otsu(\'"'+user_name+'"\',"'+str(input_type)+'",\'"'+str(file)+'"\');exit"')
            	    
		    mail_to_user = 'sendmail ' + user_email_id + ' < /home/NANOMINE/Production/mdcs/Otsu/email.html'
		    os.system(mail_to_user)
		    os.system('sendmail back2akshay@gmail.com < /home/NANOMINE/Production/mdcs/Otsu/email.html')
		    form = DocumentForm()
		    documents = Document.objects.all()
                    return render_to_response("Submission_notify.html",{'documents': documents, 'form': form}, context_instance=RequestContext(request))
		else:
		    return HttpResponse('<h3>Please upload an image!</h3>') # if no image was uploaded, report error
	  else:
		form = DocumentForm()
		documents = Document.objects.all()
		return render_to_response('Otsu_submit_image.html',{'documents': documents, 'form': form},context_instance=RequestContext(request))
	else:
		return redirect('/login')
