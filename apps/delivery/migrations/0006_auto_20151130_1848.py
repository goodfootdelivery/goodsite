# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_auto_20151130_1846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courier',
            old_name='courier',
            new_name='courier_id',
        ),
        migrations.AddField(
            model_name='order',
            name='courier',
            field=models.ForeignKey(to='delivery.Courier', null=True),
        ),
    ]
