# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_auto_20160420_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('google_id', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('comments', models.CharField(max_length=2000, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='company',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='address',
            name='saved',
            field=models.CharField(default=b'PI', max_length=10, null=True, choices=[(b'PI', b'Pickup'), (b'DR', b'Dropoff')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='service',
            field=models.CharField(default=b'BASIC', max_length=10, choices=[(b'BASIC', b'Basic'), (b'EXPRESS', b'Express')]),
        ),
        migrations.AddField(
            model_name='address',
            name='place',
            field=models.ForeignKey(to='delivery.Place', null=True),
        ),
    ]
