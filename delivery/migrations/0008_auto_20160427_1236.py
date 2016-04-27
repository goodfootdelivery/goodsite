# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_auto_20160424_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='place',
            field=models.ForeignKey(blank=True, to='delivery.Place', null=True),
        ),
    ]
