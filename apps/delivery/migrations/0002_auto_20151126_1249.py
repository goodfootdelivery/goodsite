# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='courier',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2),
        ),
        migrations.AddField(
            model_name='order',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'RE', max_length=2, choices=[(b'RE', b'Recieved'), (b'AS', b'Assigned'), (b'DE', b'Delivered'), (b'PD', b'Paid')]),
        ),
    ]
