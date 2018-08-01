# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('XMLCONV', '0002_auto_20180601_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to=b'/home/NANOMINE/Develop/mdcs/static/XMLCONV/uploads/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='templatefile',
            field=models.FileField(null=True, upload_to=b'/home/NANOMINE/Develop/mdcs/static/XMLCONV/uploads/'),
        ),
    ]
