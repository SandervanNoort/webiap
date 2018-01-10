#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2013 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Percentage of all ILI case who GP/Home/..."""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

from .figure import Figure


def Control(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        return ControlAll(**args)
    else:
        return ControlSeason(**args)


class ControlSeason(Figure):
    """Create a comparison with other sources"""

    def __init__(self, **args):
        # country, season, control_id, casedef_id

        Figure.__init__(self, args)
        self.figname = "{base}_{control_id}_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize:co}

            title_labels = control, casedef
            control_id = {control_id}
            casedef_id = {casedef_id}

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                left_ax = inet_incidence
                ymax2 = 100
                ymin = 0

                date_format = {month}
                xlabel = <<season:{season}>>
                grid = {grid}
                wrap = {wrap}
                plot_start = {plot_start}
                plot_end = {plot_end}
                {ymax_line}
        [datasets]
            [[ili]]
                source_measure = inet_incidence
                label = <<casedef:{casedef_id}>>

                country = {country}
                subset = {subset}
                season = {season}
                color = {inet_color}
                linewidth = {inet_lw}
                min_participants = {min_participants}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                intake = {intake}
                reload = {reload}
            [[control]]
                source_measure = inet_control
                bar = True
                daily = False

                country = {country}
                subset = {subset}
                season = {season}
                color = {control_color}
                min_participants = {min_participants}
                casedef = {casedef}
                casedef_id = {casedef_id}
                control = {control}
                control_id = {control_id}
                label = <<control:{control_id}>>
                intake = {intake}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)
        self.params["control_color"] = self.params[
            "{control_id}_color".format(**self.params)]
        if self.params["control_id"] == "workrate":
            self.params["intake"] = "q400_2=1"
        elif self.params["control_id"] == "schoolrate":
            self.params["intake"] = "q400_1=1"
        else:
            self.params["intake"] = ""


class ControlAll(Figure):
    """Percentage of ili cases which fit a control measure"""

    def __init__(self, **args):
        # country, control_id, casedef_id

        Figure.__init__(self, args)
        self.figname = "{base}_{control_id}_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            ax_margins_extra = 0, 0, 20, 0
            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize:co}

            city_labels = season,
            legend_labels = season,
            title_labels = control, casedef
            control_id = {control_id}
            casedef_id = {casedef_id}
            short = True

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                type = barplot
                bars = control
                xlabel_id = season

                ymax = {ymax}
                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[control]]
                source_measure = inet_control

                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                color = {control_color}
                casedef = {casedef}
                casedef_id = {casedef_id}
                control = {control}
                control_id = {control_id}
                intake = {intake}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)
        self.params["control_color"] = self.params[
            "{control_id}_color".format(**self.params)]
        if "work" in self.params["control_id"]:
            self.params["intake"] = "q400_2=1"
            self.params["ymax"] = 60
        elif "school" in self.params["control_id"]:
            self.params["intake"] = "q400_1=1"
            self.params["ymax"] = 60
        else:
            self.params["intake"] = ""
            self.params["ymax"] = 100
