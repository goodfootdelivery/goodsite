# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20160302_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='postal',
            field=models.CharField(max_length=10, null=True, validators=[django.core.validators.RegexValidator(regex=b'[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ] ?[0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]')]),
        ),
    ]
