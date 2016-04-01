# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('easypost_id', models.CharField(max_length=200, null=True)),
                ('rate_id', models.CharField(max_length=200, null=True)),
                ('tracking_code', models.CharField(max_length=100, null=True)),
                ('postal_label', models.URLField(null=True)),
                ('status', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='easypost_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='postal_label',
        ),
        migrations.RemoveField(
            model_name='order',
            name='rate_id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='tracking_code',
        ),
        migrations.AlterField(
            model_name='order',
            name='service',
            field=models.CharField(max_length=2, null=True, choices=[(b'EXPRESS', b'Express'), (b'BASIC', b'Basic')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'RE', max_length=10, choices=[(b'RE', b'Recieved'), (b'AS', b'Assigned'), (b'TR', b'In Transit'), (b'DE', b'Delivered'), (b'PD', b'Paid')]),
        ),
        migrations.AddField(
            model_name='order',
            name='shipment',
            field=models.OneToOneField(null=True, blank=True, to='delivery.Shipment'),
        ),
    ]
