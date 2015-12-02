# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0003_auto_20151130_1734'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order_Meta',
            new_name='OrderMeta',
        ),
    ]
