#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db import models


class ScanDateManager(models.Manager):
    def get_by_natural_key(self, datetime):
        return self.get(datetime=datetime)


class ScanDate(models.Model):
    datetime = models.DateTimeField(auto_created=True)
    has_errors = models.BooleanField()
    licenses_keys = models.ManyToManyField("License", through="Licenses")
    copyright_holders_keys = models.ManyToManyField("Holder", through="CopyrightHolder")
    packages_keys = models.ManyToManyField("Package", through="Version")

    objects = ScanDateManager()

    def natural_key(self):
        return (self.datetime,)

    def __str__(self):
        return f"{self.datetime}" if not self.has_errors else f"{self.datetime} [XXX]"


class LicenseCategoryManager(models.Manager):
    def get_by_natural_key(self, category):
        return self.get(category=category)


class LicenseCategory(models.Model):
    category = models.CharField(max_length=63, unique=True)

    objects = LicenseCategoryManager()

    def natural_key(self):
        return (self.category,)

    def __str__(self):
        return f"{self.category}"


class LicenseManager(models.Manager):
    def get_by_natural_key(self, spdx_license_key):
        return self.get(spdx_license_key=spdx_license_key)


class License(models.Model):
    spdx_license_key = models.CharField(max_length=127, unique=True)
    spdx_url = models.URLField(unique=True)
    category_key = models.ForeignKey(LicenseCategory, on_delete=models.PROTECT)

    objects = LicenseManager()

    def natural_key(self):
        return (self.spdx_license_key,)

    def __str__(self):
        return f"{self.spdx_license_key}"


class FilePathManager(models.Manager):
    def get_by_natural_key(self, path):
        return self.get(path=path)


class FilePath(models.Model):
    path = models.CharField(max_length=511, unique=True)

    objects = FilePathManager()

    def natural_key(self):
        return (self.path,)

    def __str__(self):
        return f"{self.path}"


class ScoreManager(models.Manager):
    def get_by_natural_key(self, score):
        return self.get(score=score)


class Score(models.Model):
    score = models.FloatField(unique=True)

    objects = ScoreManager()

    def natural_key(self):
        return (self.score,)

    def __str__(self):
        return f"{self.score}"


class LicensesManager(models.Manager):
    def get_by_natural_key(self, license_key, score_key, file_key, date_key):
        return self.get(
            license_key=license_key,
            score_key=score_key,
            file_key=file_key,
            date_key=date_key,
        )


class Licenses(models.Model):
    license_key = models.ForeignKey(License, on_delete=models.PROTECT)
    score_key = models.ForeignKey(Score, on_delete=models.PROTECT)
    file_key = models.ForeignKey(FilePath, on_delete=models.PROTECT)
    date_key = models.ForeignKey(ScanDate, on_delete=models.PROTECT)

    objects = LicensesManager()

    def natural_key(self):
        return (self.license_key, self.score_key, self.file_key, self.date_key)


class HolderManager(models.Manager):
    def get_by_natural_key(self, value):
        return self.get(value=value)


class Holder(models.Model):
    value = models.CharField(max_length=127, unique=True)

    objects = HolderManager()

    def natural_key(self):
        return (self.value,)

    def __str__(self):
        return f"{self.value}"


class CopyrightHolderManager(models.Manager):
    def get_by_natural_key(self, holder_key, file_key, date_key):
        return self.get(holder_key=holder_key, file_key=file_key, date_key=date_key)


class CopyrightHolder(models.Model):
    holder_key = models.ForeignKey(Holder, on_delete=models.PROTECT)
    file_key = models.ForeignKey(FilePath, on_delete=models.PROTECT)
    date_key = models.ForeignKey(ScanDate, on_delete=models.PROTECT)

    objects = CopyrightHolderManager()

    def natural_key(self):
        return (self.holder_key, self.file_key, self.date_key)


class PackageManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Package(models.Model):
    name = models.CharField(max_length=127, unique=True)
    file_key = models.ForeignKey(FilePath, on_delete=models.PROTECT)

    objects = PackageManager()

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return f"{self.name}"


class VersionManager(models.Manager):
    def get_by_natural_key(self, version):
        return self.get(version=version)


class Version(models.Model):
    package_key = models.ForeignKey(Package, on_delete=models.PROTECT)
    version = models.CharField(max_length=15, unique=True)
    date_key = models.ForeignKey(ScanDate, on_delete=models.PROTECT)

    objects = VersionManager()

    def natural_key(self):
        return (self.version,)

    def __str__(self):
        return f"{self.version}"
