#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : quenv/migrations/0001_initial.py
#
#       Creation Date : Fri 31 Jul 2020 10:51:23 PM EEST (22:51)
#
#       Last Modified :
#
# ==============================================================================

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Date",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("check_date", models.DateField(verbose_name="Check Date")),
            ],
            options={
                "verbose_name": "Check Date",
                "verbose_name_plural": "Check Dates",
            },
        ),
        migrations.CreateModel(
            name="Environment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "environment_name",
                    models.CharField(
                        max_length=31, unique=True, verbose_name="Environment Name"
                    ),
                ),
            ],
            options={
                "verbose_name": "Environment",
                "verbose_name_plural": "Environments",
            },
        ),
        migrations.CreateModel(
            name="Grade",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "level",
                    models.CharField(max_length=3, unique=True, verbose_name="Level"),
                ),
                (
                    "ordering",
                    models.PositiveSmallIntegerField(blank=True, verbose_name="Order"),
                ),
            ],
            options={"verbose_name": "Grade", "verbose_name_plural": "Grades"},
        ),
        migrations.CreateModel(
            name="License",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "license_name",
                    models.CharField(
                        max_length=63, unique=True, verbose_name="License Name"
                    ),
                ),
            ],
            options={"verbose_name": "License", "verbose_name_plural": "Licenses"},
        ),
        migrations.CreateModel(
            name="Package",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "package_name",
                    models.CharField(
                        max_length=31, unique=True, verbose_name="Package Name"
                    ),
                ),
            ],
            options={"verbose_name": "Package", "verbose_name_plural": "Packages"},
        ),
        migrations.CreateModel(
            name="Info",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("lines", models.PositiveIntegerField(verbose_name="Lines of Code")),
                (
                    "date_key",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="quenv.Date",
                        verbose_name="Date Checked",
                    ),
                ),
                (
                    "environment_key",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="quenv.Environment",
                        verbose_name="Environment",
                    ),
                ),
                (
                    "grade_key",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="quenv.Grade",
                        verbose_name="Grade",
                    ),
                ),
                (
                    "license_description",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="quenv.License",
                        verbose_name="License Description",
                    ),
                ),
                (
                    "licenses_keys",
                    models.ManyToManyField(
                        related_name="packages",
                        to="quenv.License",
                        verbose_name="Licenses",
                    ),
                ),
                (
                    "package_key",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="quenv.Package",
                        verbose_name="Package",
                    ),
                ),
            ],
            options={
                "verbose_name": "Installation Info",
                "verbose_name_plural": "Installation Info",
            },
        ),
        migrations.CreateModel(
            name="IncrementalChanges",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "license_changed",
                    models.BooleanField(verbose_name="Changed License"),
                ),
                ("added", models.BooleanField(verbose_name="Added")),
                ("removed", models.BooleanField(verbose_name="Removed")),
                (
                    "date_key",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="quenv.Date",
                        verbose_name="Date Checked",
                    ),
                ),
                (
                    "package_key",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="quenv.Package",
                        verbose_name="Package",
                    ),
                ),
            ],
            options={
                "verbose_name": "Incremental Changes",
                "verbose_name_plural": "Incremental Changes",
            },
        ),
    ]
