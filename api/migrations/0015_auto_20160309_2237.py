# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20160309_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(default=b'CA', max_length=2),
        ),
        migrations.AlterField(
            model_name='address',
            name='owner',
            field=models.ForeignKey(related_name='addresses', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='postal',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(regex=b'[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ] ?[0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]')]),
        ),
        migrations.AlterField(
            model_name='address',
            name='prov',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='unit',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
