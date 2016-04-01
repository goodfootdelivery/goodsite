# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_auto_20160331_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='service',
            field=models.CharField(max_length=10, null=b'BASIC', choices=[(b'BASIC', b'Basic'), (b'EXPRESS', b'Express')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'RE', max_length=2, choices=[(b'RE', b'Recieved'), (b'AS', b'Assigned'), (b'TR', b'In Transit'), (b'DE', b'Delivered'), (b'PD', b'Paid')]),
        ),
    ]
