#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : quenv/models.py
#
#       Creation Date : Sat 20 Apr 2019 08:39:37 PM EEST (20:39)
#
#       Last Modified : Mon 06 May 2019 08:46:20 PM EEST (20:46)
#
# ==============================================================================

from django.db import models
from gettext import gettext as _
from quenv import managers


class License(models.Model):
    license_name = models.CharField(
        verbose_name=_("License Name"), max_length=63, unique=True
    )

    objects = managers.LicenseManager()

    def __str__(self):
        return "{0}".format(self.license_name)

    def natural_key(self):
        return (self.license_name,)

    class Meta:
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")


class Package(models.Model):
    package_name = models.CharField(
        verbose_name=_("Package Name"), max_length=31, unique=True
    )

    objects = managers.PackageManager()

    def __str__(self):
        return "{0}".format(self.package_name)

    def natural_key(self):
        return (self.package_name,)

    class Meta:
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")


class Environment(models.Model):
    environment_name = models.CharField(
        verbose_name=_("Environment Name"), max_length=31, unique=True
    )

    objects = managers.EnvironmentManager()

    def __str__(self):
        return "{0}".format(self.environment_name)

    def natural_key(self):
        return (self.environment_name,)

    class Meta:
        verbose_name = _("Environment")
        verbose_name_plural = _("Environments")


class Grade(models.Model):
    level = models.CharField(verbose_name=_("Level"), max_length=3, unique=True)
    ordering = models.PositiveSmallIntegerField(verbose_name=_("Order"), blank=True)

    objects = managers.GradeManager()

    def __str__(self):
        return "{0}".format(self.level)

    def natural_key(self):
        return (self.level,)

    class Meta:
        verbose_name = _("Grade")
        verbose_name_plural = _("Grades")


class Date(models.Model):
    check_date = models.DateField(verbose_name=_("Check Date"))

    objects = managers.DateManager()

    def natural_key(self):
        return (self.check_date.strftime("%Y-%m-%d"),)

    def __str__(self):
        return "{0}".format(self.check_date.strftime("%Y-%m-%d"))

    class Meta:
        verbose_name = _("Check Date")
        verbose_name_plural = _("Check Dates")


class Info(models.Model):
    environment_key = models.ForeignKey(
        Environment, verbose_name=_("Environment"), on_delete=models.PROTECT
    )
    package_key = models.ForeignKey(
        Package, verbose_name=_("Package"), on_delete=models.PROTECT
    )
    license_description = models.ForeignKey(
        License, verbose_name=_("License Description"), on_delete=models.PROTECT
    )
    lines = models.PositiveIntegerField(verbose_name=_("Lines of Code"))
    grade_key = models.ForeignKey(
        Grade, verbose_name=_("Grade"), on_delete=models.PROTECT
    )
    licenses_keys = models.ManyToManyField(
        License, verbose_name=_("Licenses"), related_name="packages"
    )
    date_key = models.ForeignKey(
        Date, verbose_name=_("Date Checked"), on_delete=models.PROTECT
    )

    objects = managers.InfoManager()

    def __str__(self):
        return "Installation id: {0}".format(self.id)

    def natural_key(self):
        return (
            tuple()
            + self.date_key.natural_key()
            + self.environment_key.natural_key()
            + self.package_key.natural_key()
        )

    natural_key.dependencies = ["quenv.environment", "quenv.package", "quenv.date"]

    class Meta:
        verbose_name = _("Installation Info")
        verbose_name_plural = _("Installation Info")


class IncrementalChanges(models.Model):
    package_key = models.ForeignKey(
        Package, verbose_name=_("Package"), on_delete=models.PROTECT
    )
    license_changed = models.BooleanField(verbose_name=_("Changed License"))
    added = models.BooleanField(verbose_name=_("Added"))
    removed = models.BooleanField(verbose_name=_("Removed"))
    date_key = models.ForeignKey(
        Date, verbose_name=_("Date Checked"), on_delete=models.PROTECT
    )

    def __str__(self):
        return "Change id: {0}".format(self.id)

    def natural_key(self):
        return (
            (self.date,) + self.package_key.natural_key() + self.date_key.natural_key()
        )

    natural_key.dependencies = ["quenv.package", "quenv.date"]

    class Meta:
        verbose_name = _("Incremental Changes")
        verbose_name_plural = _("Incremental Changes")
