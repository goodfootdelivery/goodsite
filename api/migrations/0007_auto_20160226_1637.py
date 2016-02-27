# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20160226_0428'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='local',
            field=models.BooleanField(default=True),
        ),
    ]
