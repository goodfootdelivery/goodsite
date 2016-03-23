# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=12, null=True)),
                ('street', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=20, null=True)),
                ('city', models.CharField(max_length=50)),
                ('prov', models.CharField(max_length=20)),
                ('postal', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(regex=b'[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ] ?[0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]')])),
                ('country', models.CharField(default=b'CA', max_length=2)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('lng', models.FloatField(null=True, blank=True)),
                ('owner', models.ForeignKey(related_name='addresses', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('delivery_date', models.DateField()),
                ('delivery_time', models.TimeField(null=True)),
                ('comments', models.CharField(max_length=200, blank=True)),
                ('price', models.FloatField(null=True)),
                ('service', models.CharField(max_length=2, null=True, choices=[(b'EX', b'Express'), (b'BA', b'Basic')])),
                ('status', models.CharField(default=b'RE', max_length=2, choices=[(b'RE', b'Recieved'), (b'AS', b'Assigned'), (b'TR', b'In Transit'), (b'DE', b'Delivered'), (b'PD', b'Paid')])),
                ('easypost_id', models.CharField(max_length=200, null=True)),
                ('rate_id', models.CharField(max_length=200, null=True)),
                ('tracking_code', models.CharField(max_length=100, null=True)),
                ('postal_label', models.URLField(null=True)),
                ('courier', models.ForeignKey(related_name='courier', to=settings.AUTH_USER_MODEL, null=True)),
                ('dropoff', models.ForeignKey(related_name='end', to='delivery.Address', null=True)),
                ('owner', models.ForeignKey(related_name='orders', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('length', models.FloatField()),
                ('width', models.FloatField()),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='parcel',
            field=models.ForeignKey(to='delivery.Parcel', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='pickup',
            field=models.ForeignKey(related_name='start', to='delivery.Address', null=True),
        ),
    ]
