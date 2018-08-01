# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('XMLCONV', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='templatefile',
            field=models.FileField(null=True, upload_to=b'/home/hby/nanomine/static/XMLCONV/uploads/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to=b'/home/hby/nanomine/static/XMLCONV/uploads/'),
        ),
    ]
