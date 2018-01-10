#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2013 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""IFig package"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import os
import configobj

from . import tools


ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_DIR = os.path.join(ROOT, "config")

CONFIG = None
DIRS = None
DIAGRAMS = None


def init(mod):
    """Delayed initialization"""
    mod.CONFIG = configobj.ConfigObj(
        os.path.join(CONFIG_DIR, "config.ini"))

    if os.path.exists(os.path.join(CONFIG_DIR, "local.ini")):
        tools.cobj_update(
            mod.CONFIG,
            configobj.ConfigObj(os.path.join(CONFIG_DIR, "local.ini")))
    mod.DIRS = {
        ftype: os.path.join(ROOT, mod.CONFIG["local"]["web"], dirpath)
        for ftype, dirpath in mod.CONFIG["local"].items()}
    for ftype in ["ini", "png", "pdf", "csv"]:
        tools.create_dir(mod.DIRS[ftype])
    mod.DIAGRAMS = configobj.ConfigObj(
        os.path.join(CONFIG_DIR, "diagrams.ini"),
        configspec=os.path.join(CONFIG_DIR, "diagrams.spec"))
    tools.cobj_check(mod.DIAGRAMS)


def get_dir(ftype, lang="en"):
    """Return language specific dir"""
    if lang != "en":
        return "{0}_{1}".format(DIRS[ftype], lang)
    else:
        return DIRS[ftype]

tools.Delayed(__name__, init)
