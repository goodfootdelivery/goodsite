# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


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
                ('address', models.CharField(max_length=100, null=True)),
                ('unit', models.CharField(max_length=20, blank=True)),
                ('latitude', models.DecimalField(null=True, max_digits=60, decimal_places=30)),
                ('longitude', models.DecimalField(null=True, max_digits=60, decimal_places=30)),
                ('comments', models.CharField(max_length=200, blank=True)),
                ('saved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(default=b'RE', max_length=2, choices=[(b'RE', b'Recieved'), (b'AS', b'Assigned'), (b'TR', b'In Transit'), (b'DE', b'Delivered'), (b'PD', b'Paid')])),
                ('price', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('order', models.OneToOneField(primary_key=True, serialize=False, to='delivery.Order')),
                ('delivery_date', models.DateField(null=True)),
                ('service', models.CharField(default=None, max_length=2, choices=[(b'EX', b'Express'), (b'SD', b'Same Day'), (b'ND', b'Next Day')])),
                ('travel_time', models.DurationField(null=True)),
                ('dropoff', models.ForeignKey(related_name='end', to='delivery.Address', null=True)),
                ('pickup', models.ForeignKey(related_name='start', to='delivery.Address', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='courier',
            field=models.ForeignKey(related_name='courier', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
