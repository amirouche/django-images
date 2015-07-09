# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestImage',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('django_images.image',),
        ),
    ]
