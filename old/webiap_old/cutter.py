#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2013 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""ILI incidence in subgroups"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import iap

from .figure import Figure
from . import config, tools


def IliCutter(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        if args["cutter"].startswith("vaccin"):
            yield IliCutterAllRRR(**args)
        yield IliCutterAll(**args)
    else:
        yield IliCutterSeason(**args)


class IliCutterSeason(Figure):
    """Create a comparison with other sources"""

    def __init__(self, **args):
        # country, season, cutter, casedef_id
        Figure.__init__(self, args)

        self.figname = ("{base}_{cutter}_{average}_{casedef_id}" +
                        "{size_ext}")
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize_double:co}
            cols = {cols}
            rows = {rows}

            {age_format}
            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[pie]]
                xlabel_id = participants
                type = barplot
                bars = pie
                pietext = False
                ax_margins = 0, 0, 30, 0

                col = {pie_col}
                row = {pie_row}
                grid = {grid}
                wrap = {wrap}
                {samples}
            [[bar]]
                type = barplot
                bars = attack

                housedistance = {housedistance}
                col = {bar_col}
                row = {bar_row}
                yticks = {yticks}
                grid = {grid}
                wrap = {wrap}
                {samples}
            {rrr}
            [[plot]]
                type = plot
                ymin = 0

                col = {plot_col}
                row = {plot_row}
                date_format = {month}
                xlabel = <<season:{season}>>
                grid = {grid}
                wrap = {wrap}
                ylabel = "ILI / 100,000 {moving_average}"
                plot_start = {plot_start}
                plot_end = {plot_end}
                {samples}
        [datasets]
            [[default]]
                source_measure = inet_incidence
                linewidth = {subgroup_lw}

#                 measure_label = <<measure:incidence>> {moving_average}

                average = {average}
                daily = {inet_daily}
                marker = {inet_marker}
                country = {country}
                subset = {subset}
                season = {season}
                cutter = {cutter}
                casedef = {casedef}
                casedef_id = {casedef_id}
                min_participants = {min_participants_subgroups}
                min_samples = 15
                reload = {reload}
                {samples}
        """

    def set_params(self):
        Figure.set_params(self)

        if int(self.params["average"]) == 21:
            self.params["moving_average"] = "(3-<<extra:week_average>>)"
        elif int(self.params["average"]) == 14:
            self.params["moving_average"] = "(2-<<extra:week_average>>)"
        else:
            self.params["moving_average"] = ""

        # self.params["rrr"] = ""
        if self.params["size"] == "big":
            self.params["rows"] = "1, 1"
            self.params["cols"] = "4, 1"
            self.params["plot_col"] = 0
            self.params["plot_row"] = 101
            self.params["pie_col"] = 1
            self.params["pie_row"] = 0
            self.params["bar_col"] = 1
            self.params["bar_row"] = 1
            self.params["rrr_col"] = 2
            self.params["rrr_row"] = 0
        else:
            self.params["rows"] = "1,"
            self.params["cols"] = "10, 3, 4"
            self.params["plot_col"] = 0
            self.params["plot_row"] = 0
            self.params["pie_col"] = 1
            self.params["pie_row"] = 0
            self.params["bar_col"] = 2
            self.params["bar_row"] = 0
            self.params["rrr_col"] = 3
            self.params["rrr_row"] = 0

        if self.params["cutter"].startswith("vaccin"):
            if self.params["size"] == "big":
                self.params["cols"] = "4, 1, 1"
                self.params["bar_col"] = 112
            else:
                self.params["cols"] = "8, 2, 3, 3"

            self.params["samples"] = \
                "samples_onsets = {samples_threshold}".format(**self.params)
            self.params["rrr"] = """
                [[rrr]]
                    type = barplot
                    bars = compare
                    compare = rrr
                    compare_colors = {eiss_color},{eiss_prev},{inet_prev},\\
                                     {inet_color}
                    ylabel = "<<measure:ve>> <<measure:ve_unit>>"

                    rrr_cutter = {cutter}
                    housedistance = {housedistance}
                    col = {rrr_col}
                    row = {rrr_row}
                    yticks = {yticks}
                    grid = {grid}
                    wrap = {wrap}
                    {samples}

                """.format(**self.params)
        else:
            self.params["rrr"] = ""
            self.params["samples"] = ""

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if len(set([options["label"]
                    for options in myini.datasets.values()])) < 2:
            self.done("No subgroups")
            return False
        return True


class IliCutterAll(Figure):
    """Create a comparison with other sources"""

    def __init__(self, **args):
        # country, cutter, casedef_id

        Figure.__init__(self, args)
        self.figname = ("{base}_{cutter}_{average}_{casedef_id}" +
                        "{size_ext}")
        self.inistring = """
        [fig]
            title = auto
            legend_loc = {legend_loc}
            figsize = {figsize_double:co}
            ncol = {ncol}
            cols = {cols}
            rows = {rows}

            sum_labels = season,

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[bar]]
                type = barplot
                bars = attack

                grid = {grid}
                wrap = {wrap}
                housedistance = {housedistance}
                col = {bar_col}
                row = {bar_row}
                yticks = {yticks}
                {samples}
            [[pie]]
                type = barplot
                bars = pie
                pietext = False
                ax_margins = 0, 0, 30, 0
                xlabel_id = participants

                grid = {grid}
                col = {pie_col}
                row = {pie_row}
            [[plot]]
                date_format = year
                ymin = 0

                grid = {grid}
                wrap = {wrap}
                col = {plot_col}
                row = {plot_row}
                ylabel = "ILI / 100,000 {moving_average}"
                {samples}
        [datasets]
            [[default]]
                source_measure = inet_incidence

                average = {average}
                # measure_label = <<measure:incidence>> {moving_average}

                daily = {year_daily}
                linewidth = {year_lw}
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                cutter = {cutter}
                casedef = {casedef}
                casedef_id = {casedef_id}
                min_participants = {min_participants_subgroups}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)

        if self.params["cutter"].startswith("vaccin"):
            self.params["samples"] = \
                "samples_onsets = {samples_threshold}".format(**self.params)
        else:
            self.params["samples"] = ""

        if self.params["size"] == "big":
            self.params["rows"] = "1, 1"
            self.params["cols"] = "3, 1"
            self.params["plot_col"] = 0
            self.params["plot_row"] = 101
            self.params["pie_col"] = 1
            self.params["pie_row"] = 0
            self.params["bar_col"] = 1
            self.params["bar_row"] = 1
        else:
            self.params["rows"] = "1,"
            self.params["cols"] = "10, 3, 4"
            self.params["plot_col"] = 0
            self.params["plot_row"] = 0
            self.params["pie_col"] = 1
            self.params["pie_row"] = 0
            self.params["bar_col"] = 2
            self.params["bar_row"] = 0

        if int(self.params["average"]) == 21:
            self.params["moving_average"] = "(3-<<extra:week_average>>)"
        elif int(self.params["average"]) == 14:
            self.params["moving_average"] = "(2-<<extra:week_average>>)"
        else:
            self.params["moving_average"] = ""

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if len(set([options["label"]
                    for options in myini.datasets.values()])) < 2:
            self.done("No subgroups")
            return False
        return True


class IliCutterAllRRR(Figure):
    """Create a comparison with other sources"""

    def __init__(self, **args):
        # country, cutter, casedef_id
        Figure.__init__(self, args)

        self.figname = "{base}_{cutter}_rrr_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = "<<country:{country}>>__<<measure:ve>> for \\
                    <<casedef:{casedef_id}>>__<<cutter_{cutter}:vacgroup>>"
#             title = auto
            legend_loc = {legend_loc}
            figsize = {figsize:co}
            ncol = {ncol}

            city_labels = season,
            short = True
            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
            [[margins]]
                fig = 70, 15, 15, 15
        [plots]
            [[rrr]]
                type = barplot
                bars = compare
                ylabel = "<<measure:ve>> <<measure:ve_unit>>"
                xlabel_id = season
                compare = rrr
                compare_colors = {eiss_color}, {eiss_prev}, {inet_prev}, \\
                                 {inet_color}
                rrr_cutter = {cutter}
                housedistance = {housedistance}
                yticks = {yticks}
                grid = {grid}
                wrap = {wrap}
                ymin = -100
                ymax = 100
                {samples}
        [datasets]
            [[default]]
                source_measure = inet_incidence

                daily = {year_daily}
                linewidth = {year_lw}
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                cutter = {cutter}
                casedef = {casedef}
                casedef_id = {casedef_id}
                min_participants = {min_participants_subgroups}
                reload = {reload}
                {samples}
        """

    def set_params(self):
        Figure.set_params(self)

        self.params["samples"] = \
            "samples_onsets = {samples_threshold}".format(**self.params)

        if self.params["size"] == "big":
            self.params["rows"] = "1, 1"
            self.params["cols"] = "3, 1"
            self.params["plot_col"] = 0
            self.params["plot_row"] = 101
            self.params["pie_col"] = 1
            self.params["pie_row"] = 0
            self.params["bar_col"] = 1
            self.params["bar_row"] = 1
        else:
            self.params["rows"] = "1,"
            self.params["cols"] = "10, 3, 4"
            self.params["plot_col"] = 0
            self.params["plot_row"] = 0
            self.params["pie_col"] = 1
            self.params["pie_row"] = 0
            self.params["bar_col"] = 2
            self.params["bar_row"] = 0

        if int(self.params["average"]) == 21:
            self.params["moving_average"] = "(3-<<extra:week_average>>)"
        elif int(self.params["average"]) == 14:
            self.params["moving_average"] = "(2-<<extra:week_average>>)"
        else:
            self.params["moving_average"] = ""

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if len(set([options["label"]
                    for options in myini.datasets.values()])) < 2:
            self.done("No subgroups")
            return False
        return True


def HistCutter(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        all_cutter_answers = tools.SetList()
        for season in config.DIAGRAMS["ini"]["seasons"]:
            period = iap.utils.country_season_to_period(args["country"],
                                                        season)
            for cutter, answer in zip(
                    *iap.split.get_answers(args["cutter"], period)):
                if (cutter in iap.config.TABLE["cutter"] and
                        "nohist" in iap.config.TABLE["cutter"][cutter] and
                        answer in iap.config.TABLE["cutter"][
                            cutter]["nohist"]):
                    continue
                if (cutter in iap.config.TABLE["intake"] and
                        "nohist" in iap.config.TABLE["intake"][cutter] and
                        answer in iap.config.TABLE["intake"][
                            cutter]["nohist"]):
                    continue
                if (cutter, answer) in all_cutter_answers:
                    continue
                all_cutter_answers.append((cutter, answer))
                yield HistCutterAll(sub_cutter=cutter, sub_answer=answer,
                                    **args)
    else:
        yield HistCutterSeason(**args)


class HistCutterSeason(Figure):
    """Create a comparison with other sources"""

    def __init__(self, **args):
        # country, season, cutter
        if args["season"] == "all":
            HistCutterAll(**args)
            return

        Figure.__init__(self, args)
        self.figname = "{base}_part_{cutter}{size_ext}"

        self.inistring = """
        [fig]
            title = auto
            legend_loc = {legend_loc}
            lang = {lang}
            ncol = {ncol}
            figsize = {figsize_cutter:co}

            {age_format}
            ignore_labels = measure,city_cutter

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[bar]]
                type = barplot
                bars = percentage_by_answer
                # floors = True
                xlabel_id = age_group

                citydistance = {citydistance}
                errors = {errors}
                grid = {grid}
                wrap = {wrap}
                house_zero_nominator = False
        [datasets]
            [[default]]
                source_measure = inet_participants

                country = {country}
                subset = {subset}
                season = {season}
                cutter = {cutter}
                city_cutter = {age_distribution}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)
        if self.params["size"] == "big":
            self.params["errors"] = True
            self.params["figsize_cutter"] = self.params["figsize"]
        else:
            self.params["errors"] = False
            self.params["figsize_cutter"] = (
                self.params["figsize"]
                if self.params["cutter"].startswith("vaccin") else
                self.params["figsize_double"])

    def test(self, ini):
        if not Figure.test(self, ini):
            return False
        if len(set([(options["cutter"], options["answer"])
                    for options in ini.datasets.values()])) < 2:
            self.done("No subgroups")
            return False
        return True


class HistCutterAll(Figure):
    """Create a comparison with other sources"""

    def __init__(self, **args):
        # country, cutter, answer, title

        Figure.__init__(self, args)
        self.figname = "{base}_part_{sub_cutter}_{sub_answer}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            legend_loc = outer right
            ncol = 2
            lang = {lang}
            figsize = {figsize_double:co}

            ignore_labels = measure, city_cutter
            {age_format}

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[bar]]
                type = barplot
                bars = percentage_by_answer
                xlabel_id = age_group

                citydistance = {citydistance}
                errors = {errors}
                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[default]]
                source_measure = inet_participants
                cutter = {sub_cutter}
                answer = "{sub_answer}"
                city_cutter = {age_distribution}
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                reload = {reload}
            """

    def set_params(self):
        Figure.set_params(self)
#         self.params["label_fname"] = tools.normalize(
#               self.params["answer"])
        if self.params["size"] == "big":
            self.params["errors"] = True
        else:
            self.params["errors"] = False

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
#         if len(set([options["piece"]
#                 for options in myini.datasets.values()])) < 2:
#             self.done("No subgroups")
#             return False
        return True
