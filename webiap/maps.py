#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2013 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Create maps"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

from .figure import Figure


class Maps(Figure):
    """Casedef in comparison with previous season"""

    def __init__(self, **args):
        # country, season, casedef_id

        Figure.__init__(self, args)
        if args["season"] == "all":
            return

        if args["casedef_id"] not in ["ilit", "corona"] or args["country"] != "nl":
            # only maps for nl/be with ilit definition
            return

        self.figname = "{base}_map_{casedef_id}"
        self.inistring = """
        [fig]
            ignore_labels = country,
            lang = {lang}
        [map]
            mapname = nb2
            min_pixels = 1000
            min_incidence = {min_incidence}
            max_incidence = {max_incidence}
            max_color = 255, 0, 0, 255
            min_color = 255, 220, 220, 255
            none_color = 180, 180, 180, 255
            unknown_color = 220, 220, 220, 255
            fontfamily = Arial.ttf
            lang = {lang}
            pre_days = 7
            [[font]]
                date = 18 # 24
                legend = 16 # 20
                logo = 15 # 20
            [[legend]]
                ymin = 70 # 100
                height = 100 # 150
                width = 15 # 20
            [[margin]]
                date = 10
                logo = 5
                legend = 6 # 10
            [[movie]]
                bitrate = 1800
                framerate = 1
                ext = mp4
        [plots]
            [[map]]
                type = map
                [[[regions]]]
                    region1 = Groningen,Friesland,Drenthe,Overijssel
                    region2 = Noord-Holland,
                    region3 = Zuid-Holland,
                    region4 = Utrecht,Gelderland,Flevoland
                    region5 = Noord-Brabant,Limburg,Zeeland
                    region6 = Oost-Vlaanderen,West-Vlaanderen
                    region7 = Antwerpen,Belgisch-Limburg,Brussel,Vlaams-Brabant
        [datasets]
            [[nb]]
                source_measure = inet_incidence
                country_values = nl,be
                season = {season}
                cutter = region
                casedef = {casedef}
                daily = False
        """
