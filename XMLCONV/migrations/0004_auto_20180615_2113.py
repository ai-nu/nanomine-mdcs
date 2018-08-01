# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('XMLCONV', '0003_auto_20180614_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to=b'/home/NANOMINE/Production/mdcs/static/XMLCONV/uploads/'),
        ),
        migrations.AlterField(
            model_name='document',
            name='templatefile',
            field=models.FileField(null=True, upload_to=b'/home/NANOMINE/Production/mdcs/static/XMLCONV/uploads/'),
        ),
    ]
