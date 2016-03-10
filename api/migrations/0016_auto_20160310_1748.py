# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20160309_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='easypost_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='postal_label',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='rate_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='service',
            field=models.CharField(max_length=2, null=True, choices=[(b'EX', b'Express'), (b'BA', b'Basic')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='tracking_code',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
