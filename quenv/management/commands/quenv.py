#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ==============================================================================
#
#       File Name : quenv/management/commands/quenv.py
#
#       Creation Date : Mon 06 May 2019 09:01:59 PM EEST (21:01)
#
#       Last Modified : Mon 06 May 2019 09:06:41 PM EEST (21:06)
#
# ==============================================================================

from django.core.management.base import BaseCommand
from quenv.licenses import Dump

class Command(BaseCommand):
    help = 'Scans the active python environment for installed packages, their quality and their licenses'

    def handle(self, *args, **options):
        obj = Dump()
        obj.dump()

        self.stdout.write(self.style.SUCCESS('Successfully creted all quenv fixtures'))
