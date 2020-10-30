#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2012 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Generate black regions"""

from __future__ import division, absolute_import, unicode_literals

import iap.fig

inistring = """
    [map]
        mapname = nb
    """

myini = iap.Ini(inistring)
imap = iap.fig.FigMap(myini.settings)
imap.make_black_regions("/tmp/black")
