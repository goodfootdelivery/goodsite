# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('freshbooks_id', models.CharField(max_length=10000)),
                ('email', models.EmailField(max_length=30)),
                ('first_name', models.CharField(max_length=10000)),
                ('last_name', models.CharField(max_length=10000)),
                ('organization', models.CharField(max_length=10000)),
                ('phone', models.CharField(max_length=10000)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('freshbooks_id', models.CharField(max_length=10000)),
                ('sent_date', models.DateField()),
                ('status', models.CharField(default=b'CR', max_length=2, choices=[(b'CR', b'Created'), (b'SE', b'Sent'), (b'PA', b'Paid')])),
                ('client', models.ForeignKey(to='invoicing.Client')),
            ],
        ),
    ]
