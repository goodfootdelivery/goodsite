# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20160209_0505'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='postal_code',
            new_name='postal',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='region',
            new_name='prov',
        ),
    ]
