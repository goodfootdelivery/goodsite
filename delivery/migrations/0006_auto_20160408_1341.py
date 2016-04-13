# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_auto_20160404_0223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipment',
            old_name='price',
            new_name='cost',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipment',
        ),
        migrations.AddField(
            model_name='address',
            name='easypost_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='easypost_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shipment',
            name='order',
            field=models.OneToOneField(null=True, blank=True, to='delivery.Order'),
        ),
    ]
