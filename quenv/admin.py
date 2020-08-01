#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : quenv/admin.py
#
#       Creation Date : Sat 20 Apr 2019 08:39:37 PM EEST (20:39)
#
#       Last Modified : Sat 01 Aug 2020 10:56:41 PM EEST (22:56)
#
# ==============================================================================

from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from gettext import gettext as _
from quenv import models


class LicenseListFilter(admin.SimpleListFilter):
    title = _("License in Description or Classifier")
    parameter_name = "license"

    def lookups(self, request, model_admin):
        licenses = models.License.objects.all().order_by("license_name")
        for each in licenses:
            yield (each.license_name, each.license_name)

    def queryset(self, request, queryset):

        if self.value():
            search_terms = Q(
                Q(license_description__license_name=self.value())
                | Q(licenses_keys__license_name=self.value())
            )
            return queryset.filter(search_terms).distinct()


@admin.register(models.Info)
class InfoAdmin(admin.ModelAdmin):
    list_filter = ("environment_key__environment_name", LicenseListFilter)
    list_select_related = True
    date_hierarchy = "date_key__check_date"
    list_display = (
        "packages",
        "license",
        "lines",
        "grade_key_level",
        "changes_link",
    )

    @staticmethod
    def packages(obj):
        return obj.package_key.package_name

    packages.admin_order_field = "package_key__package_name"

    @staticmethod
    def license(obj):
        # url = reverse("admin:quenv_license_changelist")
        # return format_html(
        #     "<a href={0}?packages__id={1}>{2}</a>", url, obj.id, obj.license_description
        # )
        return obj.license_description

    license.short_description = _("License Description")
    license.admin_order_field = "license_description__license_name"

    @staticmethod
    def grade_key_level(obj):
        return obj.grade_key.level

    grade_key_level.admin_order_field = "grade_key__ordering"

    @staticmethod
    def changes_link(obj):
        url = reverse("admin:quenv_incrementalchanges_changelist")
        return format_html(
            "<a href={0}?date_key__check_date__day={1}&date_key__check_date__month={2}&date_key__check_date__year={3}>Related Changes</a>",
            url,
            obj.date_key.check_date.day,
            obj.date_key.check_date.month,
            obj.date_key.check_date.year,
        )

    changes_link.short_description = _("Related Changes")

    @staticmethod
    def has_add_permission(request):
        return False

    @staticmethod
    def has_change_permission(request, obj=None):
        return False

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False


# @admin.register(models.License)
# class LicenseAdmin(admin.ModelAdmin):
#     list_display = ("license_name", "packages_link")
#
#     @staticmethod
#     def packages_link(obj):
#         url = reverse("admin:quenv_info_changelist")
#         return format_html(
#             "<a href={0}?license={1}>Related Packages</a>",
#             url,
#             obj.license_name.replace(" ", "+"),
#         )
#
#     packages_link.short_description = _("Related Packages")
#
#     @staticmethod
#     def has_add_permission(request):
#         return False
#
#     @staticmethod
#     def has_change_permission(request, obj=None):
#         return False
#
#     @staticmethod
#     def has_delete_permission(request, obj=None):
#         return False
#
#     @staticmethod
#     def has_view_permission(request, obj=None):
#         return False
#
#
# @admin.register(models.Package)
# class PackageAdmin(admin.ModelAdmin):
#     list_display = ("package_name",)
#
#     @staticmethod
#     def has_add_permission(request):
#         return False
#
#     @staticmethod
#     def has_change_permission(request, obj=None):
#         return False
#
#     @staticmethod
#     def has_delete_permission(request, obj=None):
#         return False
#
#     @staticmethod
#     def has_view_permission(request, obj=None):
#         return False
#
#
# @admin.register(models.Environment)
# class EnvironmentAdmin(admin.ModelAdmin):
#     @staticmethod
#     def has_add_permission(request):
#         return False
#
#     @staticmethod
#     def has_change_permission(request, obj=None):
#         return False
#
#     @staticmethod
#     def has_delete_permission(request, obj=None):
#         return False
#
#     @staticmethod
#     def has_view_permission(request, obj=None):
#         return False


# @admin.register(models.Date)
# class DateAdmin(admin.ModelAdmin):
#     list_display = ("check_date", "packages_link", "changes_link")
#
#     @staticmethod
#     def packages_link(obj):
#         url = reverse("admin:quenv_info_changelist")
#         return format_html(
#             "<a href={0}?date_key__check_date__day={1}&date_key__check_date__month={2}&date_key__check_date__year={3}>Related Packages</a>",
#             url,
#             obj.check_date.day,
#             obj.check_date.month,
#             obj.check_date.year,
#         )
#
#     packages_link.short_description = _("Related Packages")
#
#     @staticmethod
#     def changes_link(obj):
#         url = reverse("admin:quenv_incrementalchanges_changelist")
#         return format_html(
#             "<a href={0}?date_key__check_date__day={1}&date_key__check_date__month={2}&date_key__check_date__year={3}>Related Changes</a>",
#             url,
#             obj.check_date.day,
#             obj.check_date.month,
#             obj.check_date.year,
#         )
#
#     changes_link.short_description = _("Related Changes")
#
#     @staticmethod
#     def has_add_permission(request):
#         return False
#
#     @staticmethod
#     def has_change_permission(request, obj=None):
#         return False
#
#     @staticmethod
#     def has_delete_permission(request, obj=None):
#         return False


# @admin.register(models.Grade)
# class GradeAdmin(admin.ModelAdmin):
#     ordering = ["ordering"]
#
#     @staticmethod
#     def has_add_permission(request):
#         return False
#
#     @staticmethod
#     def has_change_permission(request, obj=None):
#         return False
#
#     @staticmethod
#     def has_delete_permission(request, obj=None):
#         return False
#
#     @staticmethod
#     def has_view_permission(request, obj=None):
#         return False


@admin.register(models.IncrementalChanges)
class IncrementalChangesAdmin(admin.ModelAdmin):
    date_hierarchy = "date_key__check_date"
    list_display = (
        "package_key",
        "license_changed",
        "added",
        "removed",
        "packages_link",
    )

    @staticmethod
    def packages_link(obj):
        url = reverse("admin:quenv_info_changelist")
        return format_html(
            "<a href={0}?date_key__check_date__day={1}&date_key__check_date__month={2}&date_key__check_date__year={3}>Related Installation</a>",
            url,
            obj.date_key.check_date.day,
            obj.date_key.check_date.month,
            obj.date_key.check_date.year,
        )

    packages_link.short_description = _("Installation Packages")

    @staticmethod
    def has_add_permission(request):
        return False

    @staticmethod
    def has_change_permission(request, obj=None):
        return False

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False
