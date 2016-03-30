# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='sent_date',
            new_name='date_sent',
        ),
        migrations.AddField(
            model_name='invoice',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2016, 3, 30, 16, 26, 19, 846179, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(default=b'CR', max_length=2, choices=[(b'CR', b'Created'), (b'BL', b'Billable'), (b'SE', b'Sent'), (b'PA', b'Paid')]),
        ),
    ]
