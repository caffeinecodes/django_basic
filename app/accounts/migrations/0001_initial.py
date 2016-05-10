# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('first_name', models.CharField(max_length=30, null=True, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='last name', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('receive_newsletter', models.BooleanField(default=False, verbose_name='receive newsletter')),
                ('facebook_id', models.CharField(max_length=30, blank=True)),
                ('activation_key', models.CharField(max_length=40, blank=b'True')),
                ('reset_password_key', models.CharField(max_length=40, blank=b'True')),
                ('key_expires', models.DateTimeField(default=datetime.datetime(2015, 12, 8, 9, 18, 19, 187543))),
                ('is_email_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name=b'user', related_name='tmp_user_set', verbose_name='groups', to='auth.Group', blank=True)),
                ('user_permissions', models.ManyToManyField(related_query_name=b'user', related_name='tmp_user_set', verbose_name='user permissions', to='auth.Permission', blank=True)),
            ],
            options={
                'db_table': 'accounts',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
