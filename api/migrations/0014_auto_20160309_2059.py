# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20160302_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(default=b'CA', max_length=2, blank=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='prov',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
