# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0003_auto_20160401_1403'),
        ('delivery', '0003_auto_20160401_1453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='owner',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='owner',
            new_name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='invoice_id',
            field=models.ForeignKey(blank=True, to='invoicing.Invoice', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='invoice_line',
            field=models.CharField(max_length=5000, null=True),
        ),
    ]
