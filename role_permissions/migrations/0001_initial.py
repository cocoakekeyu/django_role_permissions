# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-10 10:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractBaseRole',
            fields=[
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.Group')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='角色名称')),
                ('is_active', models.BooleanField(default=True, verbose_name='状态')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'auth_role',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('abstractbaserole_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='role_permissions.AbstractBaseRole')),
            ],
            bases=('role_permissions.abstractbaserole',),
        ),
    ]
