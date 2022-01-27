#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from pydantic import BaseModel


"""
[
    {
        "model": "quenv.scandate",
        "fields": {
            "datetime": "2022-01-19T19:02:29Z",
            "has_errors": false
        }
    },
    {
        "model": "quenv.licensecategory",
        "fields": {
            "category": "Permissive"
        }
    },
    {
        "model": "quenv.license",
        "fields": {
            "spdx_license_key": "BSD-3-Clause",
            "spdx_url": "https://spdx.org/licenses/BSD-3-Clause",
            "category_key": [
                "Permissive"
            ]
        }
    },
    {
        "model": "quenv.filepath",
        "fields": {
            "path": ".venv/lib/python3.9/site-packages/MarkupSafe-2.0.1.dist-info/METADATA"
        }
    },
    {
        "model": "quenv.score",
        "fields": {
            "score": 100.0
        }
    },
    {
        "model": "quenv.score",
        "fields": {
            "score": 99.0
        }
    },
    {
        "model": "quenv.licenses",
        "fields": {
            "license_key": [
                "BSD-3-Clause"
            ],
            "score_key": [
                100.0
            ],
            "file_key": [
                ".venv/lib/python3.9/site-packages/MarkupSafe-2.0.1.dist-info/METADATA"
            ],
            "date_key": [
                "2022-01-19T19:02:29Z"
            ]
        }
    },
    {
        "model": "quenv.licenses",
        "fields": {
            "license_key": [
                "BSD-3-Clause"
            ],
            "score_key": [
                99.0
            ],
            "file_key": [
                ".venv/lib/python3.9/site-packages/MarkupSafe-2.0.1.dist-info/METADATA"
            ],
            "date_key": [
                "2022-01-19T19:02:29Z"
            ]
        }
    },
    {
        "model": "quenv.holder",
        "fields": {
            "value": "IPython Development Team"
        }
    },
    {
        "model": "quenv.copyrightholder",
        "fields": {
            "holder_key": [
                "IPython Development Team"
            ],
            "file_key": [
                ".venv/lib/python3.9/site-packages/MarkupSafe-2.0.1.dist-info/METADATA"
            ],
            "date_key": [
                "2022-01-19T19:02:29Z"
            ]
        }
    },
    {
        "model": "quenv.package",
        "fields": {
            "name": "MarkupSafe",
            "file_key": [
                ".venv/lib/python3.9/site-packages/MarkupSafe-2.0.1.dist-info/METADATA"
            ]
        }
    },
    {
        "model": "quenv.version",
        "fields": {
            "package_key": [
                "MarkupSafe"
            ],
            "version": "2.0.1",
            "date_key": [
                "2022-01-19T19:02:29Z"
            ]
        }
    }
]

"""

from typing import Dict
from pydantic import BaseModel, Field, root_validator, validator

from quenv.djantic import LicenseCategorySchema, LicenseSchema, ScanDateSchema


class LicensePreparation(BaseModel):
    model: str = "quenv.licenses"
    fields: LicenseSchema


class LicensesPerFile(BaseModel):
    '''
    one_file_licenses = data["files"][5818]
    f = LicensesPerFile(**licenses)
    f.dict()
    prints:
    {
        "licenses": [
            {
                "model": "quenv.licenses",
                "fields": {
                    "spdx_license_key": "GPL-1.0-or-later",
                    "spdx_url": "https://spdx.org/licenses/GPL-1.0-or-later",
                    "category_key": ["Copyleft"],
                },
            },
            {
                "model": "quenv.licenses",
                "fields": {
                    "spdx_license_key": "GPL-1.0-or-later",
                    "spdx_url": "https://spdx.org/licenses/GPL-1.0-or-later",
                    "category_key": ["Copyleft"],
                },
            },
        ]
    }
    '''
    licenses: list[LicensePreparation]

    @validator("licenses", pre=True)
    def prepare_licenses(cls, v):
        return [LicensePreparation(fields=each) for each in v]


class AllAround(BaseModel):
    '''
    dict() returns:
    {
        "files": [
            {
                "model": "quenv.licenses",
                "fields": {
                    "spdx_license_key": "MIT-CMU",
                    "spdx_url": "https://spdx.org/licenses/MIT-CMU",
                    "category_key": [
                        "Permissive"
                    ]
                }
            },
            {
                ...
            },
        ]
    }

    '''
    files: list

    @validator("files", pre=True)
    def prepare_licenses(cls, v):
        # Here, extend the data that will build the fixture
        licenses = []
        for each in v:
            licenses.extend(LicensesPerFile(**each).licenses)
        return licenses
