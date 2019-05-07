#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : quenv/management/commands/quenv.py
#
#       Creation Date : Mon 06 May 2019 09:01:59 PM EEST (21:01)
#
#       Last Modified : Tue 07 May 2019 12:13:29 PM EEST (12:13)
#
# ==============================================================================

from django.core.management.base import BaseCommand, CommandError
from gettext import gettext as _
from quenv.licenses import Dump


class Command(BaseCommand):
    help = _(
        "Scans the active python environment for installed packages, reports their licenses and quality"
    )

    def handle(self, *args, **options):
        obj = Dump()
        try:
            obj.dump()
        except FileExistsError:
            raise CommandError(
                _(
                    "Quenv operates only once per day. A fixture for today already exists."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(_("Successfully creted all quenv fixtures"))
        )
