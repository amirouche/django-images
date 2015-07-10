# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('kind', models.CharField(max_length=255)),
                ('uid', models.CharField(max_length=255)),
                ('json_xs', models.TextField()),
                ('json_sm', models.TextField()),
                ('json_md', models.TextField()),
                ('json_lg', models.TextField()),
                ('json_og', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ContentImage',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('django_images.image',),
        ),
        migrations.CreateModel(
            name='CoverImage',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('django_images.image',),
        ),
        migrations.CreateModel(
            name='LogoImage',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('django_images.image',),
        ),
        migrations.CreateModel(
            name='PictoImage',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('django_images.image',),
        ),
    ]
