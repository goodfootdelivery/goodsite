# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.IntegerField(serialize=False, primary_key=True)),
                ('user', models.CharField(max_length=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(default=b'RE', max_length=2, choices=[(b'RE', b'Recieved'), (b'AS', b'Assigned'), (b'DE', b'Delivered')])),
            ],
        ),
    ]
