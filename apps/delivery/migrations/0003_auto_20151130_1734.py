# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delivery', '0002_auto_20151126_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_Meta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('courier', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='courier',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'RE', max_length=2, choices=[(b'RE', b'Recieved'), (b'AS', b'Assigned'), (b'TR', b'In Transit'), (b'DE', b'Delivered'), (b'PD', b'Paid')]),
        ),
    ]
