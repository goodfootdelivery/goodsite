# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_auto_20151222_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('length', models.CharField(default=b'RE', max_length=200, choices=[(b'RE', b'Recieved'), (b'AS', b'Assigned'), (b'TR', b'In Transit'), (b'DE', b'Delivered'), (b'PD', b'Paid')])),
                ('width', models.CharField(default=b'RE', max_length=200, choices=[(b'RE', b'Recieved'), (b'AS', b'Assigned'), (b'TR', b'In Transit'), (b'DE', b'Delivered'), (b'PD', b'Paid')])),
                ('height', models.CharField(default=b'RE', max_length=200, choices=[(b'RE', b'Recieved'), (b'AS', b'Assigned'), (b'TR', b'In Transit'), (b'DE', b'Delivered'), (b'PD', b'Paid')])),
                ('weight', models.CharField(default=b'RE', max_length=200, choices=[(b'RE', b'Recieved'), (b'AS', b'Assigned'), (b'TR', b'In Transit'), (b'DE', b'Delivered'), (b'PD', b'Paid')])),
            ],
        ),
        migrations.RemoveField(
            model_name='address',
            name='saved',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dist_mat',
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(),
        ),
        migrations.AddField(
            model_name='order',
            name='parcel',
            field=models.OneToOneField(null=True, to='delivery.Parcel'),
        ),
    ]
