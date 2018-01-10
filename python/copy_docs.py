#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2012 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Copy the intake and survey questions"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import os
import shutil

from ifig import tools
import iap

ROOT = os.path.join(os.path.dirname(__file__), "..")
for table in ["intake", "survey"]:
    shutil.copy(os.path.join(iap.CONFIG_DIR, "{0}.ini".format(table)),
                os.path.join(ROOT, "data"))
for lang in os.listdir(os.path.join(iap.CONFIG_DIR, "lang")):
    for fname in os.listdir(os.path.join(iap.CONFIG_DIR, "lang", lang)):
        tools.create_dir(os.path.join(ROOT, "data", "lang", lang))
        shutil.copy(os.path.join(iap.CONFIG_DIR, "lang", lang, fname),
                    os.path.join(ROOT, "data", "lang", lang))
