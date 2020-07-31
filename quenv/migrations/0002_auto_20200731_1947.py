#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : quenv/migrations/0002_auto_20200731_1947.py
#
#       Creation Date : Fri 31 Jul 2020 10:51:23 PM EEST (22:51)
#
#       Last Modified :
#
# ==============================================================================

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quenv", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="environment",
            name="environment_name",
            field=models.CharField(
                max_length=63, unique=True, verbose_name="Environment Name"
            ),
        ),
        migrations.AlterField(
            model_name="license",
            name="license_name",
            field=models.CharField(
                max_length=127, unique=True, verbose_name="License Name"
            ),
        ),
        migrations.AlterField(
            model_name="package",
            name="package_name",
            field=models.CharField(
                max_length=63, unique=True, verbose_name="Package Name"
            ),
        ),
    ]
