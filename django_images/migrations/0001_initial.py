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
                ('ptype', models.SmallIntegerField(choices=[[1, b'Background image'], [3, b'Picto'], [2, b'Content image'], [4, b'Logo']])),
                ('name', models.CharField(max_length=255)),
                ('ext', models.CharField(max_length=5)),
                ('xs_width', models.SmallIntegerField()),
                ('xs_height', models.SmallIntegerField()),
                ('sm_width', models.SmallIntegerField()),
                ('sm_height', models.SmallIntegerField()),
                ('md_width', models.SmallIntegerField()),
                ('md_height', models.SmallIntegerField()),
                ('lg_width', models.SmallIntegerField()),
                ('lg_height', models.SmallIntegerField()),
                ('og_width', models.SmallIntegerField()),
                ('og_height', models.SmallIntegerField()),
            ],
        ),
    ]
