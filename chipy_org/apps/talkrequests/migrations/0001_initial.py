# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TalkCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'Talk Category',
                'verbose_name_plural': 'Talk Categories',
            },
        ),
        migrations.CreateModel(
            name='TalkRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64)),
                ('text', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('recent_date', models.DateField(help_text=b'When was this last talked about?', null=True, blank=True)),
                ('category', models.ForeignKey(blank=True, to='talkrequests.TalkCategory', null=True)),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Talk Request',
                'verbose_name_plural': 'Talk Requests',
            },
        ),
        migrations.CreateModel(
            name='TalkVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('ip_address', models.CharField(max_length=64)),
                ('talk_request', models.ForeignKey(to='talkrequests.TalkRequest')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Talk Vote',
                'verbose_name_plural': 'Talk Votes',
            },
        ),
    ]
