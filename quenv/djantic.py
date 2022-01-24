#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional
from djantic import ModelSchema
from quenv import models
from pydantic import Field, validator, root_validator, BaseModel


class ScanDateSchema(ModelSchema):
    class Config:
        model = models.ScanDate
        include = ("has_errors", "id")


class LicenseCategorySchema(ModelSchema):
    class Config:
        model = models.LicenseCategory
        exclude = ("id", "license")


class LicenseSchema(ModelSchema):
    category_key: str = Field(alias="category")

    class Config:
        model = models.License
        exclude = ("id", "scandate", "licenses")
        allow_population_by_field_name = True

    @validator("category_key")
    def category_key_validation(cls, value):
        return [value]


class FilePathSchema(ModelSchema):
    class Config:
        model = models.FilePath


class ScoreSchema(ModelSchema):
    class Config:
        model = models.Score


class LicensesSchema(ModelSchema):
    date_key: ScanDateSchema

    class Config:
        model = models.Licenses
        exclude = ("id",)


class CopyrightHolderSchema(ModelSchema):
    class Config:
        model = models.CopyrightHolder


class HolderSchema(ModelSchema):
    class Config:
        model = models.Holder


class PackageSchema(ModelSchema):
    class Config:
        model = models.Package


class VersionSchema(ModelSchema):
    class Config:
        model = models.Version
