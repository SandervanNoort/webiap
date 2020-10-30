#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2012 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Copy the intake and survey questions"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import os
import re

import iap
import webiap
from webiap import tools


def copy_ini(fname_in, fname_out):
    fobj_in = open(fname_in, 'r')
    fobj_out = open(fname_out, 'w')
    tools.create_dir(fname_out)
    for line in fobj_in:
        # TODO: this fails for hash tags inside the value
        line = re.sub("#", ";", line)
        fobj_out.write(line)
    fobj_in.close()
    fobj_out.close()


ROOT = os.path.join(os.path.dirname(__file__), "..")
for table in ["intake", "survey"]:
    fname = "{0}.ini".format(table)
    copy_ini(
        os.path.join(iap.config.CONFIG_DIR, "{0}.ini".format(table)),
        os.path.join(webiap.config.get_dir("data"), "{0}.ini".format(table)))
for lang in os.listdir(os.path.join(iap.config.CONFIG_DIR, "lang")):
    for fname in os.listdir(os.path.join(iap.config.CONFIG_DIR, "lang", lang)):
        copy_ini(
            os.path.join(iap.config.CONFIG_DIR, "lang", lang, fname),
            os.path.join(webiap.config.get_dir("data"), "lang", lang, fname))
