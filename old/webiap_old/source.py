#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2013 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Various non Influenzanet sources"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import iap

from .figure import Figure
from . import config


def Europe(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["source"] in ("google", "eiss"):
        return ILI(**args)
    elif args["source"] in ("climate",):
        return Other(**args)


def ILI(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        yield ILIAll(**args)
        if args["source"] == "eiss":
            yield EissAll(**args)
    else:
        yield ILISeason(**args)
        if args["source"] == "eiss":
            yield Eiss(**args)


class ILISeason(Figure):
    """Create a Graph of non-inet ili source with previous year"""

    def __init__(self, **args):
        # country, source, season

        Figure.__init__(self, args)
        self.figname = "{base}_prev_{source}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize:co}

            legend_labels = season,

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                ymin = 0

                date_format = {month}
                grid = {grid}
                wrap = {wrap}
                plot_start = {plot_start}
                plot_end = {plot_end}
        [datasets]
            [[previous]]
                source_measure = {source}_{measure}
                casedef = {casedef}
                casedef_id = {casedef}
                country = {country}
                subset = {subset}
                season = {season_prev}
                color = {prev_color}
                linewidth = {lw}
                marker = {ili_marker}
                daily = {ili_daily}
                markersize = {markersize}
            [[current]]
                source_measure = {source}_{measure}
                casedef = {casedef}
                casedef_id = {casedef}
                country = {country}
                subset = {subset}
                season = {season}
                color = {current_color}
                linewidth = {lw}
                marker = {ili_marker}
                daily = {ili_daily}
                markersize = {markersize}
        """

    def set_params(self):
        Figure.set_params(self)
        self.params["season_prev"] = iap.utils.prev_season(
            self.params["season"])
        self.params["current_color"] = \
            self.params["{source}_color".format(**self.params)]
        self.params["prev_color"] = \
            self.params["{source}_prev".format(**self.params)]
        if self.params["source"] == "eiss":
            self.params["measure"] = "incidence"
            if self.params["country"] in config.DIAGRAMS["params"]["ari"]:
                self.params["casedef"] = "ari"
            else:
                self.params["casedef"] = "ili"
        elif self.params["source"] == "google":
            self.params["measure"] = "trends"
            self.params["casedef"] = ""

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if self.params["season"] not in [
                options["season"] for options in myini.datasets.values()]:
            self.done("No current season")
            return False
        return True


class Eiss(Figure):
    """Create a Graph with virus confirmation"""

    def __init__(self, **args):
        # country, source, season

        Figure.__init__(self, args)
        if args["season"] == "all":
            return

        self.figname = "{base}_full_eiss{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize:co}

            ignore_labels = measure,

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                ymin = 0

                date_format = {month}
                xlabels = <<season:{season}>>
                grid = {grid}
                wrap = {wrap}
                plot_start = {plot_start}
                plot_end = {plot_end}
                xlabel = <<season:{season}>>
                allow_empty = eiss_samples,
        [datasets]
            {eiss_ili}
            [[infa]]
                source_measure = eiss_samples
                casedef = {infa}
                country = {country}
                subset = {subset}
                season = {season}
                color = {infa_color}
                bar = True
            [[infb]]
                source_measure = eiss_samples
                casedef = {infb}
                country = {country}
                subset = {subset}
                season = {season}
                color = {infb_color}
                bar = True
        """

    def set_params(self):
        Figure.set_params(self)
        self.params["current_color"] = \
            self.params["{source}_color".format(**self.params)]
        if self.params["country"] in config.DIAGRAMS["params"]["ari"]:
            self.params["casedef"] = "ari"
        else:
            self.params["casedef"] = "ili"

        self.params["eiss_ili"] = """
        [[ili]]
            source_measure = eiss_incidence
            country = {country}
            subset = {subset}
            season = {season}
            casedef = {casedef}
            casedef_id = {casedef}
            color = {eiss_color}
            linewidth = {lw}
            marker = {ili_marker}
            daily = {ili_daily}
            markersize = {markersize}""".format(**self.params)
        self.params["infa"] = "infa"
        self.params["infb"] = "infb"
#         else:
#             self.params["infa"] = "infa"
#             self.params["infb"] = "infb"
#             self.params["eiss_ili"] = ""


class EissAll(Figure):
    """Create a Graph with virus confirmation"""

    def __init__(self, **args):
        # country, source, season

        Figure.__init__(self, args)
        self.figname = "{base}_full_eiss{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize_double:co}

            ignore_labels = measure, season

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                date_format = year
                ymin = 0

                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[ili]]
                source_measure = eiss_incidence
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                casedef = {casedef}
                casedef_id = {casedef}
                color = {eiss_color}
                linewidth = {year_lw}
            [[infa]]
                source_measure = eiss_samples
                casedef = infa
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                color = {infa_color}
                bar = True
            [[infb]]
                source_measure = eiss_samples
                casedef = infb
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                color = {infb_color}
                bar = True
        """

    def set_params(self):
        Figure.set_params(self)
        self.params["current_color"] = \
            self.params["{source}_color".format(**self.params)]
        if self.params["country"] in config.DIAGRAMS["params"]["ari"]:
            self.params["casedef"] = "ari"
        else:
            self.params["casedef"] = "ili"


class ILIAll(Figure):
    """All month comparison of non-inet ili source"""

    def __init__(self, **args):
        # country, source

        Figure.__init__(self, args)
        self.figname = "{base}_month_{source}{size_ext}"
        self.inistring = """
        [fig]
            title = auto

            lang = {lang}
            figsize = {figsize_double:co}
            legend_loc = {legend_loc_all}
            ncol = {ncol_all}

            legend_labels = season,

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                ymin = 0

                grid = {grid}
                wrap = {wrap}
                date_format = {month}
                plot_start = {plot_start}
                plot_end = {plot_end}
        [datasets]
            [[default]]
                source_measure = {source}_{measure}
                casedef = {casedef}
                casedef_id = {casedef}
                color = mix

                country = {country}
                subset = {subset}
                season_values = {seasons_reversed:co}
                linewidth = {month_lw}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)
        if self.params["source"] == "google":
            self.params["casedef"] = ""
            self.params["measure"] = "trends"
        elif self.params["source"] == "eiss":
            self.params["measure"] = "incidence"
            if self.params["country"] in config.DIAGRAMS["params"]["ari"]:
                self.params["casedef"] = "ari"
            else:
                self.params["casedef"] = "ili"


def Other(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        return OtherAll(**args)
    else:
        return OtherSeason(**args)


class OtherSeason(Figure):
    """Create a Graph of non-inet non-ili source with previous year"""

    def __init__(self, **args):
        # country, source, season

        Figure.__init__(self, args)
        self.figname = "{base}_prev_{source}{size_ext}"
        self.inistring = """
        [fig]
            title = auto

            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize:co}

            legend_labels = season,

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                date_format = {month}
                grid = {grid}
                wrap = {wrap}
                plot_start = {plot_start}
                plot_end = {plot_end}
        [datasets]
            [[previous]]
                source_measure = {source}_{measure}
                country = {country}
                subset = {subset}
                season = {season_prev}
                color = {prev_color}
                linewidth = {lw}
                marker = {other_marker}
                daily = {other_daily}
                markersize = {markersize}
            [[current]]
                source_measure = {source}_{measure}
                country = {country}
                subset = {subset}
                season = {season}
                color = {current_color}
                linewidth = {lw}
                marker = {other_marker}
                daily = {other_daily}
                markersize = {markersize}
        """

    def set_params(self):
        Figure.set_params(self)
        self.params["season_prev"] = iap.utils.prev_season(
            self.params["season"])
        self.params["current_color"] = \
            self.params["{source}_color".format(**self.params)]
        self.params["prev_color"] = \
            self.params["{source}_prev".format(**self.params)]
        self.params["source"] = "climate"
        self.params["measure"] = "temp"

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if self.params["season"] not in [
                options["season"] for options in myini.datasets.values()]:
            self.done("No current season")
            return False
        return True


class OtherAll(Figure):
    """All month comparison of non-inet ili source"""

    def __init__(self, **args):
        # country, source

        Figure.__init__(self, args)
        self.figname = "{base}_month_{source}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            figsize = {figsize_double:co}
            legend_loc = {legend_loc_all}
            ncol = {ncol_all}

            legend_labels = season,

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                grid = {grid}
                wrap = {wrap}
                date_format = {month}
                plot_start = {plot_start}
                plot_end = {plot_end}
        [datasets]
            [[default]]
                source_measure = {source}_{measure}
                color = mix

                country = {country}
                subset = {subset}
                season_values = {seasons_reversed:co}
                linewidth = {month_lw}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)
        if self.params["source"] == "climate":
            self.params["source"] = "climate"
            self.params["measure"] = "temp"


def Compare(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["compare"] in ("eiss", "google"):
        return ILICompare(**args)
    elif args["compare"] in ("climate",):
        return OtherCompare(**args)


def ILICompare(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        return ILICompareAll(**args)
    else:
        return ILICompareSeason(**args)


class ILICompareSeason(Figure):
    """Create a comparison with other ILI source (eiss/google)"""

    def __init__(self, **args):
        # country, season, compare, casedef_id

        Figure.__init__(self, args)
        self.figname = "{base}_{compare}_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize:co}
            lang = {lang}

            title_labels = casedef, measure
            ignore_labels = measure,

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
                {ymax_line}

                linreg_intercept0 = {linreg_intercept0}
                linreg_sources = inet_incidence, {compare}_{measure}
                linreg_casedefs = "{casedef}", "{sm_casedef}"
                linreg_seasons = {linreg_seasons:co}
                linreg_country = {country}
        [datasets]
            [[inet]]
                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = {inet_color}
                band_color = {inet_band}
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[other]]
                source_measure = {compare}_{measure}
                color = {sm_color}
                limits = show

                season = {season}
                country = {country}
                subset = {subset}
                linewidth = {lw}
                casedef = {sm_casedef}
                casedef_id = {casedef_id}
                daily = {ili_daily}
                marker = {ili_marker}
                markersize = {markersize}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)
        self.params["sm_color"] = self.params["{compare}_color".format(
            **self.params)]
        if self.params["compare"] == "google":
            self.params["sm_casedef"] = ""
            self.params["measure"] = "trends"
        if self.params["compare"] == "eiss":
            self.params["measure"] = "incidence"
            if self.params["country"] in config.DIAGRAMS["params"]["ari"]:
                self.params["sm_casedef"] = "ari"
            else:
                self.params["sm_casedef"] = "ili"

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if len(set([options["label"]
                    for options in myini.datasets.values()])) < 2:
            self.done("No comparison")
            return False
        return True


class ILICompareAll(Figure):
    """Create a comparison with other ILI source"""

    def __init__(self, **args):
        # country, compare, casedef_id

        Figure.__init__(self, args)
        self.figname = "{base}_{compare}_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize_double:co}

            title_labels = casedef, measure
            ignore_labels = season, measure

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

                linreg_r2 = True
                linreg_intercept0 = {linreg_intercept0}
                linreg_sources = inet_incidence, {compare}_{measure}
                linreg_casedefs = "{casedef}", "{sm_casedef}"
                linreg_seasons = {linreg_seasons:co}
                linreg_country = {country}
                {ymax_line}
        [datasets]
            [[inet]]
                source_measure = inet_incidence
                daily = {year_daily}
                season_values = {seasons:co}
                country = {country}
                subset = {subset}
                color = {inet_color}
                band_color = {inet_band}
                min_participants = {min_participants}
                linewidth = {year_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                reload = {reload}
            [[other]]
                source_measure = {compare}_{measure}
                season_values = {seasons:co}
                country = {country}
                subset = {subset}
                color = {sm_color}
                linewidth = {year_lw}
                casedef_id = {casedef_id}
                casedef = {sm_casedef}
                daily = {year_daily}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)
        self.params["sm_color"] = self.params["{compare}_color".format(
            **self.params)]
        if self.params["compare"] == "google":
            self.params["sm_casedef"] = ""
            self.params["measure"] = "trends"
        if self.params["compare"] == "eiss":
            self.params["measure"] = "incidence"
            if self.params["country"] in config.DIAGRAMS["params"]["ari"]:
                self.params["sm_casedef"] = "ari"
            else:
                self.params["sm_casedef"] = "ili"

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if len(set([options["label"]
                    for options in myini.datasets.values()])) < 2:
            self.done("No comparison")
            return False
        return True


def OtherCompare(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        return OtherCompareAll(**args)
    else:
        return OtherCompareSeason(**args)


class OtherCompareSeason(Figure):
    """Create a comparison with other non-ili source"""

    def __init__(self, **args):
        # country, season, compare, casedef_id

        Figure.__init__(self, args)
        self.figname = "{base}_{compare}_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize:co}
            lang = {lang}

            title_labels = measure, casedef

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
                {ymax_line}
        [datasets]
            [[inet]]
                source_measure = inet_incidence
                label = <<casedef:{casedef_id}>>

                season = {season}
                country = {country}
                subset = {subset}
                color = {inet_color}
                band_color = {inet_band}
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[other]]
                source_measure = {source}_{measure}
                color = {sm_color}
                limits = show

                season = {season}
                country = {country}
                subset = {subset}
                linewidth = {lw}
                daily = {other_daily}
                marker = {other_marker}
                markersize = {markersize}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)
        self.params["sm_color"] = self.params["{compare}_color".format(
            **self.params)]
        self.params["source"] = "climate"
        self.params["measure"] = "temp"

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if len(set([options["label"]
                    for options in myini.datasets.values()])) < 2:
            self.done("No comparison")
            return False
        return True


class OtherCompareAll(Figure):
    """Create a comparison with other (non-ili) sources"""

    def __init__(self, **args):
        # country, compare, casedef_id

        Figure.__init__(self, args)

        self.figname = "{base}_{compare}_{casedef_id}{size_ext}"

        self.inistring = """
        [fig]
            title = auto
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize_double:co}

            ignore_labels = season,
            title_labels = measure, casedef

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
                {ymax_line}
        [datasets]
            [[inet]]
                source_measure = inet_incidence
                label = <<casedef:{casedef_id}>>

                daily = {year_daily}
                season_values = {seasons:co}
                country = {country}
                subset = {subset}
                color = {inet_color}
                band_color = {inet_band}
                min_participants = {min_participants}
                linewidth = {year_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                reload = {reload}
            [[other]]
                source_measure = {source}_{measure}
                season_values = {seasons:co}
                country = {country}
                subset = {subset}
                color = {sm_color}
                linewidth = {year_lw}
                daily = {year_daily}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)
        self.params["sm_color"] = self.params["{compare}_color".format(
            **self.params)]
        self.params["source"] = "climate"
        self.params["measure"] = "temp"

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if len(set([options["label"]
                    for options in myini.datasets.values()])) < 2:
            self.done("No comparison")
            return False
        return True
