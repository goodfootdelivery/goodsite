# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_name', models.CharField(max_length=30, blank=True)),
                ('contact_number', models.CharField(max_length=12, blank=True)),
                ('formatted', models.CharField(max_length=100, null=True)),
                ('number', models.CharField(max_length=100, null=True)),
                ('street', models.CharField(max_length=100, null=True)),
                ('locality', models.CharField(max_length=100, null=True)),
                ('post_code', models.CharField(max_length=10, null=True)),
                ('region', models.CharField(max_length=100, null=True)),
                ('country', models.CharField(max_length=100, null=True)),
                ('location', models.CharField(max_length=100, null=True, blank=True)),
                ('unit', models.CharField(max_length=20, blank=True)),
                ('comments', models.CharField(max_length=200, null=True, blank=True)),
                ('saved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('delivery_date', models.DateField(null=True)),
                ('status', models.CharField(default=b'RE', max_length=2, choices=[(b'RE', b'Recieved'), (b'AS', b'Assigned'), (b'TR', b'In Transit'), (b'DE', b'Delivered'), (b'PD', b'Paid')])),
                ('service', models.CharField(default=None, max_length=2, choices=[(b'EX', b'Express'), (b'SD', b'Same Day'), (b'ND', b'Next Day')])),
                ('dist_mat', jsonfield.fields.JSONField(default=dict)),
                ('courier', models.ForeignKey(related_name='courier', to=settings.AUTH_USER_MODEL)),
                ('dropoff', models.ForeignKey(related_name='end', to='delivery.Address', null=True)),
                ('pickup', models.ForeignKey(related_name='start', to='delivery.Address', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('length', models.FloatField(null=True)),
                ('width', models.FloatField(null=True)),
                ('height', models.FloatField(null=True)),
                ('weight', models.FloatField(null=True)),
                ('local', models.BooleanField(default=False)),
                ('order', models.ForeignKey(to='delivery.Order', null=True)),
            ],
        ),
    ]
