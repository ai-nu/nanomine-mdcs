# Bingyin Hu 05252018
from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .forms import *

import os, random, getpass
from XMLCONV.models import Document
from XMLCONV.forms import DocumentForm
from time import gmtime, strftime
from operator import itemgetter

import time, math, glob
import numpy as np

import os.path
import csv
# Create your views here.

# xsdfile = 'PNC_schema_060718.xsd'
# ParentDir = os.environ['NM_WEB_STATIC']
ParentDir = '/home/NANOMINE/Production/mdcs/static'
# ParentDir = '/home/NANOMINE/ONR/Converter_web/archive/'

def home(request):
    if request.user.is_authenticated():
        global timestamp, excel_file, img_file
        timestamp = strftime("%Y%M%d%H%M%S", gmtime())
        # define archive directory and source code directory here
        archiveDir = ParentDir + '/XMLCONV/archive/' # uploaded files will be copied here to the WorkingDir
        codeDir = ParentDir + '/XMLCONV/code_src/' # code will be copied from here to the WorkingDir
        upDir_init = ParentDir + '/XMLCONV/uploads/'# define the initial upload directory
        upDir = ParentDir + '/XMLCONV/uploads/' + timestamp + '/'# define the final upload directory
        mediaDir = ParentDir + '/XMLCONV/media/' # directory for media uploads
        removeAll = 'rm -r ' + upDir # the command that cleans the upload directory
        messages = [] # initialize the feedback messages
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                # create the timestamp folder
                os.system('mkdir -p ' + upDir)
                # template file
                tfile = request.FILES.getlist('templatefile')[0]
                newtemp = Document(templatefile = tfile)
                newtemp.save()
                # other files
                dfiles = request.FILES.getlist('docfile')
                for dfile in dfiles:
                    newdoc = Document(docfile = dfile)
                    newdoc.save()
                # move everything into the timestamp folder
                move2ts = 'find ' + upDir_init + ' -maxdepth 1 -type f -print0 | xargs -0 mv -t ' + upDir
                os.system(move2ts)
                # copy source code to the upload directory
                os.system('cp -avr ' + codeDir + '* ' + upDir)
                # get the name of the template file
                excel_file = request.FILES['templatefile'].name
                # validate the file extension
                ext = os.path.splitext(excel_file)[1] # [0] returns path+filename
                if ext.lower() not in ['.xlsx', '.xls']:
                    messages = ['[Upload Error] The Excel template file should have extensions like ".xlsx" or ".xls".']
                    # remove everything
                    os.system(removeAll)
                    return render(request, 'XMLCONV.html', {'form': form, 'messages': messages}, context_instance=RequestContext(request))
                # move to upDir and run extract_verify_ID.py to extract ID
                toUpDir = 'cd ' + upDir + ';'
                call_start = "python extract_verify_ID.py %s" %(excel_file)
                os.system(toUpDir + call_start)
                # make sure ID.txt is there
                if not os.path.exists(upDir + 'ID.txt'):
                    if os.path.exists(upDir + 'error_message.txt'):
                        with open(upDir + 'error_message.txt', 'r+') as f:
                            error_message = f.read()
                        # read the error message
                        messages_raw = error_message.split('\n')
                        for message in messages_raw:
                            if len(message.strip()) > 0:
                                messages.append(message.strip())    
                    messages += ['[Upload Error] Oops! Something wrong with the uploaded Excel template file. Please check or contact the administrator!']
                    # remove everything
                    os.system(removeAll)
                    return render(request, 'XMLCONV.html', {'form': form, 'messages': messages}, context_instance=RequestContext(request))
                # open ID.txt generated in upDir to decide next step
                with open(upDir + 'ID.txt', 'r+') as fid:
                    ID = fid.read()
                # otherwise ID.txt contains the verified Sample ID
                PID = ID.split('_')[0]
                SID = ID.split('_')[1]
                # create the working directory, now all the files are saved under archive/PID/SID/timestamp
                WorkingDir = archiveDir + PID + '/' + SID + '/'
                if not os.path.exists(WorkingDir):
                    os.makedirs(WorkingDir)
                    print '---------------------------Created working folder'
                
                # move uploads/timestamp to WorkingDir
                mvfile = 'mv ' + upDir + ' '+ WorkingDir
                # mvfile = 'mv ./XMLCONV/media/*'+' '+ WorkingDir
                print mvfile
                os.system(mvfile)
                
                # now update WorkingDir
                WorkingDir += timestamp + '/'
                
                # write the workingdir.str
                f = open('./XMLCONV/workingdir.str', 'w+')
                f.write(WorkingDir)
                f.close()
        
                # os.system('cp -avr /home/NANOMINE/ONR/Converter_web/code_src/* '+WorkingDir)
                os.system('cp ./XMLCONV/workingdir.str '+ WorkingDir)
                                
                # run compiler code
                toPath = 'cd ' + WorkingDir + ';'
                # toPath = 'cd '+WorkingDir+'/src;'
                call_start2 = "python customized_compiler_ubuntu.py %s" %(excel_file)
                os.system(toPath + call_start2)

                # check the error_message.txt
                if os.path.exists(WorkingDir + 'error_message.txt'):
                    with open(WorkingDir + 'error_message.txt', 'r+') as f:
                        error_message = f.read()
                    # read the error message
                    messages_raw = error_message.split('\n')
                    for message in messages_raw:
                        if len(message.strip()) > 0:
                            messages.append(message.strip())    
                # see if xml_update_validator.py has generated an error_log
                csvDs = glob.glob(WorkingDir + '/*.csv')
                csvDir = '' # init the csv file directory
                for csvD in csvDs:
                    if 'xml_validation_error_log_' in csvD:
                        csvDir = csvD
                if len(csvDir) > 0:
                    with open(csvDir) as csvfile:
                        vld_log = csv.DictReader(csvfile)
                        for row in vld_log:
                            if ID in row['xml directory']:
                                if "the atomic type 'xs:double'" in row['error']:
                                    messages.append('[XML Schema Validation Error] ' + row['error'].strip() + ', should be a number.')
                                else:
                                    messages.append('[XML Schema Validation Error] ' + row['error'].strip())
                # at this point, if there is no error message generated, then proceed
                if len(messages) > 0:
                    # remove everything in the WorkingDir
                    os.system('rm -r ' + WorkingDir)
                    return render(request, 'XMLCONV.html', {'form': form, 'messages': messages}, context_instance=RequestContext(request))

                # with open(WorkingDir + '/ID.txt') as _f:
                #     doc_ID = _f.read()
                # call_start3 = "python upload_to_db.py %s" %(doc_ID)
                call_start3 = "python upload_to_db.py %s" %(ID)
                # print call_start
                # print call_start2
                os.system(toPath + call_start3)
                
                # check if the upload is successful
                if os.path.exists(WorkingDir + '/up.success'):
                   # move the images
                    all_files = glob.glob(WorkingDir + '/*.*')
                    img_file = list()
                    for f in all_files:
                        if f.split('.')[-1].lower() in ['png', 'jpg', 'tif', 'tiff', 'gif']: # added tiff, gif
                            img_file.append(f)
                    if len(img_file) > 0:
                        cmd_mkdir_media = 'mkdir -p ' + mediaDir + PID + '/' + SID + '/'
                        os.system(cmd_mkdir_media)
                        # copy image files to html folder
                        for i in img_file:
                            cpimg = 'cp '+ i + ' ' + mediaDir + PID + '/' + SID + '/'
                            os.system(cpimg)
                    # generate the success message         
                    success = 'The file is saved to the repository as "%s". Thank you!' %(ID)
                    return render(request, 'XMLCONV.html', {'form': form, 'success': success}, context_instance=RequestContext(request))
                # if the upload is unsuccessful, contact the administrator
                messages.append('Oops! It seems the upload is failed. Please check your uploads or contact the administrator.')
                return render(request, 'XMLCONV.html', {'form': form, 'messages': messages}, context_instance=RequestContext(request))

        else:
            print 'not valid'
            form = DocumentForm()
        documents = Document.objects.all()
        return render(request, 'XMLCONV.html', {'form': form}, context_instance=RequestContext(request))
    else:
        return redirect('/login')