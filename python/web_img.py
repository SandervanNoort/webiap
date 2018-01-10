#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2012 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Run the server to display images"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import cherrypy
import ifig.cherry
import os

cherrypy.quickstart(ifig.cherry.Cherry(), "/",
                    os.path.join(ifig.config.ROOT, "config", "cherrypy.ini"))
