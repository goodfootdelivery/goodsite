# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20160226_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='shipping_id',
            new_name='easypost_id',
        ),
        migrations.RemoveField(
            model_name='address',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='order',
            name='local',
        ),
        migrations.AddField(
            model_name='order',
            name='comments',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(max_length=12, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='unit',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterModelTable(
            name='address',
            table='api_address',
        ),
    ]
