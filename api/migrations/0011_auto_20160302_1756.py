# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20160302_1755'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='order',
            table='api_order',
        ),
        migrations.AlterModelTable(
            name='parcel',
            table='api_parcel',
        ),
    ]
