#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : quenv/licenses.py
#
#       Creation Date : Sun 21 Apr 2019 01:18:22 PM EEST (13:18)
#
#       Last Modified : Tue 07 May 2019 04:00:36 PM EEST (16:00)
#
# ==============================================================================

import json
import os
import requests
import sys
import time

from collections import namedtuple, defaultdict
from datetime import date
from django.conf import settings
from django.core.management import call_command
from itertools import compress
from pkg_resources import get_distribution, working_set
from quenv.models import Date, Info, IncrementalChanges
from tqdm import tqdm
from urllib.parse import urlparse


class Package:
    """
    It creates a pkg_resources.DistInfoDistribution (setuptools) object
    and extracts the necessary information from its metadata attributes
    and classifiers.
    """

    def __init__(self, package_name):
        self.pkg = get_distribution(package_name)
        self.result = namedtuple(
            "Result",
            [
                "name",
                "environment",
                "description_license",
                "classifier_licenses",
                "lgtm",
            ],
        )
        # self.result.name = '{0}-{1}'.format(self.pkg.project_name, self.pkg.version)
        self.result.name = "{0}".format(self.pkg.project_name)
        self.result.environment = sys.executable.split(os.sep)[-3]
        self.service_path = "https://lgtm.com/api/v1.0/projects/"

    def get_lgtm_result(self, url_identifier):
        """
        Query the lgtm api and get the available data if they exist.
        """
        if url_identifier:
            full_path = "{0}{1}".format(self.service_path, url_identifier)

            time.sleep(1)  # Taking it easier
            response = requests.get(full_path, headers={"Accept": "application/json"})

            if response.status_code == 200:
                for each_lang in json.loads(response.text).get("languages", []):
                    if each_lang.get("language", None) == "python":
                        return each_lang
        return {}

    def lgtm_query(self, line):
        """
        Check if a github url is present in order to query the lgtm api.
        It is possible to extend the reasons for starting a lgtm query.
        """
        url = urlparse(line[line.find("https://") :])
        whitelist = ("github.com",)
        if all(
            (
                any(
                    (
                        line.startswith("Project-URL: Source"),
                        line.startswith("Home-page"),
                    )
                ),
                url.netloc in whitelist,
            )
        ):
            return self.get_lgtm_result("g{0}".format(url.path))

        return self.get_lgtm_result(None)

    def filters(self, line):
        """
        Search in each metadata line for package licenses
        or reasons (like the string 'github.com') to start a lgtm query.
        """
        return {
            "lgtm": self.lgtm_query(line),
            "licenses": compress(
                (line[9:], line[23:].replace("OSI Approved", "").replace(" :: ", "")),
                (line.startswith("License:"), line.startswith("Classifier: License")),
            ),
        }

    def get_pkg_details(self):
        try:
            lines = self.pkg.get_metadata_lines("METADATA")
        except OSError:
            lines = self.pkg.get_metadata_lines("PKG-INFO")
        return map(self.filters, lines)

    def info(self):
        lgtm = dict()
        classifiers = list()

        for each in self.get_pkg_details():
            lgtm.update(each["lgtm"])
            classifiers.extend(filter(None, each["licenses"]))

        self.result.description_license = classifiers.pop(0)
        self.result.classifier_licenses = classifiers
        self.result.lgtm = lgtm
        return self.result


class Dump:
    """
    It creates a json dump based on the json building blocks for each model.
    It also provides default data for Grade and License models.
    """

    def __init__(self):
        self.raw_data = defaultdict(set)
        self.data = defaultdict(list)
        self.environment_packages = working_set
        self.ordering = dict(
            [
                (grade, index)
                for index, grade in enumerate(("A+", "A", "B", "C", "D", "E", "0"))
            ]
        )
        self.create_package = Package
        for k, v in self.ordering.items():
            self.raw_data[self.get_grade_obj].add((k, v))
        self.raw_data[self.get_license_obj].add("UNKNOWN")

    @staticmethod
    def get_environment_obj(environment):
        return {
            "model": "quenv.environment",
            "fields": {"environment_name": str(environment).strip()},
        }

    @staticmethod
    def get_license_obj(license_name):
        return {
            "model": "quenv.license",
            "fields": {"license_name": str(license_name).strip()},
        }

    @staticmethod
    def get_package_obj(package):
        return {
            "model": "quenv.package",
            "fields": {"package_name": str(package).strip()},
        }

    @staticmethod
    def get_date_obj():
        return {
            "model": "quenv.date",
            "fields": {"check_date": date.today().strftime("%Y-%m-%d")},
        }

    @staticmethod
    def get_grade_obj(grade, ordering=10000):
        return {
            "model": "quenv.grade",
            "fields": {"level": str(grade).strip(), "ordering": int(ordering)},
        }

    @staticmethod
    def get_info_obj(
        environment, package, description="UNKNOWN", lines=0, grade="0", licenses=None
    ):
        return {
            "model": "quenv.info",
            "fields": {
                "environment_key": [str(environment).strip()],
                "package_key": [str(package).strip()],
                "license_description": [str(description).strip()],
                "lines": int(lines),
                "grade_key": [str(grade).strip()],
                "date_key": [date.today().strftime("%Y-%m-%d")],
                "licenses_keys": [[str(l.strip())] for l in licenses]
                if licenses
                else [],
            },
        }

    def compose_data(self, package_info):
        """
        Use raw_data dict to compose the contents of the data instance variable.
        """
        self.data[self.get_date_obj].append(self.get_date_obj())

        for function, values in self.raw_data.items():
            if function == self.get_grade_obj or function == self.get_info_obj:
                self.data[function].extend(list(map(lambda x: function(*x), values)))
            else:
                self.data[function].extend(list(map(function, values)))

    def prepare_raw_data(self, package_info):
        """
        From each package info get its gathered data and distribute them to
        the raw_data instance variable in order to remove possible duplicates.
        """
        self.raw_data[self.get_license_obj].add(package_info.description_license)
        self.raw_data[self.get_package_obj].add(package_info.name)
        self.raw_data[self.get_environment_obj].add(package_info.environment)
        self.raw_data[self.get_info_obj].add(
            (
                package_info.environment,
                package_info.name,
                package_info.description_license,
                package_info.lgtm.get("lines", 0),
                package_info.lgtm.get("grade", 0),
                tuple(package_info.classifier_licenses),
            )
        )

        for each_license in package_info.classifier_licenses:
            self.raw_data[self.get_license_obj].add(each_license)

        if package_info.lgtm.get("grade", False):
            self.raw_data[self.get_grade_obj].add(
                (
                    package_info.lgtm["grade"],
                    self.ordering.get(package_info.lgtm["grade"], 10000),
                )
            )

    def get_result(self, env_packages):
        with tqdm(total=len(tuple(self.environment_packages))) as pbar:
            for each_package in env_packages:
                package_info = each_package.info()
                self.prepare_raw_data(package_info)
                pbar.update(1)
            self.compose_data(package_info)
        return (
            self.data[self.get_environment_obj]
            + self.data[self.get_license_obj]
            + self.data[self.get_date_obj]
            + self.data[self.get_package_obj]
            + self.data[self.get_grade_obj]
            + self.data[self.get_info_obj]
        )

    @staticmethod
    def update_db(fixture_fullpath):
        call_command("loaddata", fixture_fullpath)
        dates = Date.objects.all().order_by("-check_date")[:2]
        difference_collection = Info.objects.filter(date_key__in=dates).values_list(
            "date_key__check_date",
            "package_key_id",
            "license_description",
            "licenses_keys",
        )
        packages = defaultdict(set)
        licenses = dict()

        for each in difference_collection:
            packages[each[0]].add(each[1])
            licenses.setdefault(each[1], {}).update({each[0]: (each[2], each[3])})
        changed_licenses = []

        for k, v in licenses.items():
            if len(v) == 2:
                if v[dates[0].check_date] != v[dates[1].check_date]:
                    changed_licenses.append(k)

        if len(dates) == 2:
            if not IncrementalChanges.objects.filter(date_key=dates[0]).exists():
                IncrementalChanges.objects.bulk_create(
                    [
                        IncrementalChanges(
                            package_key_id=i,
                            license_changed=False,
                            added=True,
                            removed=False,
                            date_key=dates[0],
                        )
                        for i in (
                            packages[dates[0].check_date].difference(
                                packages[dates[1].check_date]
                            )
                        )
                    ]
                )
                IncrementalChanges.objects.bulk_create(
                    [
                        IncrementalChanges(
                            package_key_id=i,
                            license_changed=False,
                            added=False,
                            removed=True,
                            date_key=dates[0],
                        )
                        for i in (
                            packages[dates[1].check_date].difference(
                                packages[dates[0].check_date]
                            )
                        )
                    ]
                )
                IncrementalChanges.objects.bulk_create(
                    [
                        IncrementalChanges(
                            package_key_id=i,
                            license_changed=True,
                            added=False,
                            removed=False,
                            date_key=dates[0],
                        )
                        for i in changed_licenses
                    ]
                )

    def dump(self):
        fixture_fullpath = os.path.join(
            getattr(settings, "QUENV_PATH", ""),
            "{0}.json".format(date.today().strftime("%Y-%m-%d")),
        )
        data = self.get_result(map(self.create_package, self.environment_packages))
        with open(fixture_fullpath, "x") as f:
            json.dump(data, f, indent=2)

        if getattr(settings, "QUENV_UPDATE_DB", True):
            self.update_db(fixture_fullpath)
