from django.db import models
from django.utils.encoding import smart_unicode
import os

# Create your models here.
class Document(models.Model):
    upDir = '/home/NANOMINE/Production/mdcs/static/XMLCONV/uploads/' # define the upload directory
    docfile = models.FileField(upload_to=upDir)
    # docfile = models.FileField(upload_to='./XMLCONV/media')
    templatefile = models.FileField(upload_to=upDir,null=True)
    # templatefile = models.FileField(upload_to='./XMLCONV/media',validators=[validate_file_extension],null=True)