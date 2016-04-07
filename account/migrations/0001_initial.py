# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-06 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('last_name', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(max_length=30)),
                ('profession', models.CharField(blank=True, max_length=30)),
                ('position', models.CharField(blank=True, max_length=30)),
                ('professional_experience', models.PositiveSmallIntegerField(blank=True)),
                ('driver_license', models.CharField(blank=True, choices=[('A', 'A'), ('A1', 'A1'), ('B', 'B'), ('B1', 'B1'), ('BE', 'BE'), ('C', 'C'), ('C1', 'C1'), ('CE', 'CE'), ('C1E', 'C1E'), ('D', 'D'), ('D1', 'D1'), ('DE', 'DE'), ('D1E', 'D1E'), ('M', 'M'), ('Tm', 'Tm'), ('Tb', 'Tb')], max_length=30)),
                ('driving_experience', models.IntegerField(blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Expert',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('account.myuser',),
        ),
        migrations.CreateModel(
            name='Moderator',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('account.myuser',),
        ),
    ]
