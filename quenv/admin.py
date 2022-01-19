#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib import admin

from quenv import models


@admin.register(models.ScanDate)
class ScanDateAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LicenseCategory)
class LicenseCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.License)
class LicenseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FilePath)
class FilePathAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Score)
class ScoreAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Licenses)
class LicensesAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CopyrightHolder)
class CopyrightHolderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Holder)
class HolderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Package)
class PackageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Version)
class VersionAdmin(admin.ModelAdmin):
    pass
