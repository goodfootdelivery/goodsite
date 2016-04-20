# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_auto_20160420_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ready_time_end',
            field=models.TimeField(default=b'15:34 PM'),
        ),
    ]
