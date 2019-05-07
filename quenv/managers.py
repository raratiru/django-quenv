#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : quenv/managers.py
#
#       Creation Date : Wed 24 Apr 2019 10:33:22 PM EEST (22:33)
#
#       Last Modified : Mon 06 May 2019 08:48:38 PM EEST (20:48)
#
# ==============================================================================


from django.db import models


class LicenseManager(models.Manager):
    def get_by_natural_key(self, license_name):
        return self.get(license_name=license_name)


class PackageManager(models.Manager):
    def get_by_natural_key(self, package_name):
        return self.get(package_name=package_name)


class EnvironmentManager(models.Manager):
    def get_by_natural_key(self, environment_name):
        return self.get(environment_name=environment_name)


class GradeManager(models.Manager):
    def get_by_natural_key(self, level):
        return self.get(level=level)


class DateManager(models.Manager):
    def get_by_natural_key(self, check_date):
        return self.get(check_date=check_date)


class IncrementalChangesManager(models.Manager):
    def get_by_natural_key(self, package_key, date_key):
        return self.get(package_key=package_key, date_key=date_key)


class InfoManager(models.Manager):
    def get_by_natural_key(self, date, environment, package):
        return self.get(
            date_key__check_date=date,
            environment_key__environment_name=environment,
            package_key__package_name=package,
        )
