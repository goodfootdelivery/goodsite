# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_order_ready_time_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ready_time_end',
            field=models.TimeField(default=datetime.time(15, 28, 39, 268814)),
        ),
    ]
