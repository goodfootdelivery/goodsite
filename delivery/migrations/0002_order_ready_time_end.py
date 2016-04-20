# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ready_time_end',
            field=models.TimeField(default=b'6:00 PM'),
        ),
    ]
