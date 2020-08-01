#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : quenv/migrations/0003_auto_20200801_1912.py
#
#       Creation Date : Sun 02 Aug 2020 12:53:05 AM EEST (00:53)
#
#       Last Modified :
#
# ==============================================================================

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ("quenv", "0002_auto_20200731_1947"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="date",
            options={
                "verbose_name": "View by Date",
                "verbose_name_plural": "View by Date",
            },
        ),
        migrations.AlterModelOptions(
            name="incrementalchanges",
            options={
                "verbose_name": "View Changes",
                "verbose_name_plural": "View Changes",
            },
        ),
        migrations.AlterModelOptions(
            name="info",
            options={"verbose_name": "Panorama", "verbose_name_plural": "Panorama"},
        ),
    ]
