#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Optional
from djantic import ModelSchema
from quenv import models
from pydantic import root_validator, BaseModel


class LicensesSchema(ModelSchema):
    # date_key: ScanDateSchema
    class Config:
        model = models.Licenses
        include = ("date_key",)


class Scan:
    instances = []

    def __init__(self, has_errors):
        self.has_errors = has_errors
        self.__class__.instances.append(self)

    def get_id(self):
        return int(len(self.instances))


class ScanDateSchema(ModelSchema):
    model: str = "quenv.ScanDate"
    fields: dict
    # licenses_set: LicensesSchema
    # id: Optional[int]

    class Config:
        model = models.ScanDate
        include = ("has_errors", "id")

    # @validator("has_errors")
    # def checker(cls, v):
    #     return v

    @root_validator
    def make_id(cls, values):
        the_id = Scan(values["has_errors"]).get_id()
        values["id"] = the_id

        return values


class Test(BaseModel):
    model: Optional[str] = "quenv.ScanDateSchema"
    fields: dict


class LicenseCategorySchema(ModelSchema):
    class Config:
        model = models.LicenseCategory


class LicenseSchema(ModelSchema):
    category_key: List[dict]

    class Config:
        model = models.License


class FilePathSchema(ModelSchema):
    class Config:
        model = models.FilePath


class ScoreSchema(ModelSchema):
    class Config:
        model = models.Score


# class LicensesSchema(ModelSchema):
#     date_key: ScanDateSchema
#
#     class Config:
#         model = models.Licenses
#         include = ("date_key",)


class CopyrightSchema(ModelSchema):
    class Config:
        model = models.Copyright


class CopyrightsSchema(ModelSchema):
    class Config:
        model = models.Copyrights


class PackageSchema(ModelSchema):
    class Config:
        model = models.Package


class VersionSchema(ModelSchema):
    class Config:
        model = models.Version
