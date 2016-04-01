# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0002_auto_20160330_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date_sent',
            field=models.DateField(null=True, blank=True),
        ),
    ]
