# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_auto_20151130_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='courier',
            field=models.ForeignKey(related_name='trep', to=settings.AUTH_USER_MODEL),
        ),
    ]
