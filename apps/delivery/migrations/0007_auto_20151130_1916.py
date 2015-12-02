# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_auto_20151130_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courier',
            name='courier_id',
        ),
        migrations.AlterField(
            model_name='order',
            name='courier',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Courier',
        ),
    ]
