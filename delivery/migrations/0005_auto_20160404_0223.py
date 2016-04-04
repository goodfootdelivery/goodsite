# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_auto_20160402_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='easypost_id',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]
