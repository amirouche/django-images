# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vitrine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BackgroundImage',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('django_images.image',),
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('django_images.image',),
        ),
        migrations.AddField(
            model_name='vitrine',
            name='background',
            field=models.ForeignKey(to='gallery.BackgroundImage'),
        ),
        migrations.AddField(
            model_name='vitrine',
            name='logo',
            field=models.ForeignKey(to='gallery.Logo'),
        ),
    ]
