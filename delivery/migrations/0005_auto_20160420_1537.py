# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_auto_20160420_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ready_time_end',
            field=models.TimeField(default=datetime.datetime(2016, 4, 20, 15, 37)),
        ),
    ]
