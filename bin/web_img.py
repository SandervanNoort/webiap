#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2012 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Run the server to display images"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import cherrypy
import webiap.cherry
import os

cherrypy.quickstart(webiap.cherry.Cherry(), "/",
                    os.path.join(webiap.config.ROOT, "config", "cherrypy.ini"))
