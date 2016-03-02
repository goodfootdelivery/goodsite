# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20160302_1754'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='address',
            table='api_address',
        ),
    ]
