#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2013 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Age correction"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

from .figure import Figure


def Age(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        return AgeAll(**args)
    else:
        return AgeSeason(**args)


class AgeSeason(Figure):
    """Create a comparison with other sources"""

    def __init__(self, **args):
        # country, season, age, casedef_id

        Figure.__init__(self, args)
        self.figname = "{base}_{age}_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize:co}
            lang = {lang}

            title_labels = casedef,

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                left_ax = inet_incidence
                ymin = 0

                date_format = {month}
                xlabel = <<season:{season}>>
                grid = {grid}
                wrap = {wrap}
                plot_start = {plot_start}
                plot_end = {plot_end}
        [datasets]
            [[inet]]
                source_measure = inet_incidence
                label = <<extra:standard>>

                season = {season}
                country = {country}
                subset = {subset}
                min_participants = {min_participants}
                casedef = {casedef}
                casedef_id = {casedef_id}
                color = {inet_color}

                linewidth = {inet_lw}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[age]]
                source_measure = inet_incidence
                label = <<extra:agecor>>

                season = {season}
                country = {country}
                subset = {subset}
                min_participants = {min_participants}
                casedef = {casedef}
                casedef_id = {casedef_id}
                age_correction = {age}
                color = {age_color}
                linewidth = {inet_lw}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)


class AgeAll(Figure):
    """Create a comparison with other sources"""

    def __init__(self, **args):
        # country, age, casedef_id

        Figure.__init__(self, args)

        self.figname = "{base}_{age}_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize_double:co}
            title_labels = casedef,
            city_labels = season,

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                date_format = year
                left_ax = inet_incidence
                ymin = 0

                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[inet]]
                source_measure = inet_incidence
                label = <<extra:standard>>

                daily = {year_daily}
                season_values = {seasons:co}
                country = {country}
                subset = {subset}
                color = {inet_color}
                min_participants = {min_participants}
                linewidth = {year_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
            [[corrected]]
                source_measure = inet_incidence
                label = <<extra:agecor>>

                daily = {year_daily}
                linewidth = {year_lw}
                season_values = {seasons:co}
                country = {country}
                subset = {subset}
                color = {age_color}
                min_participants = {min_participants}
                casedef = {casedef}
                casedef_id = {casedef_id}
                age_correction = {age}
        """
