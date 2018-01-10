#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2013 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Various assumptions for the ili plots"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

from .figure import Figure
from . import config


def Analysis(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    analysis = args["analysis"]
    return (None if args["season"] == "all" else
            IgnoreFirst(**args) if analysis == "ignorefirst" else
            MinSurveys(**args) if analysis == "minsurveys" else
            MaxFreq(**args) if analysis == "maxfreq" else
            AlwaysActive(**args) if analysis == "alwaysactive" else
            None)


class IgnoreFirst(Figure):
    """Create a comparison with other ILI source (eiss/google)"""

    def __init__(self, **args):
        # country, season, compare, casedef_id

        Figure.__init__(self, args)
        self.figname = "{base}_ignorefirst_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            legend_loc = outer right
            ncol = 1
            figsize = {figsize_double:co}
            lang = {lang}
            colors = {extra_colors:co}

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                left_ax = inet_incidence
                allow_empty = eiss_incidence,
                ymin = 0

                date_format = {month}
                xlabel = <<season:{season}>>
                grid = {grid}
                wrap = {wrap}
                plot_start = {plot_start}
                plot_end = {plot_end}

                linreg_intercept0 = {linreg_intercept0}
                linreg_sources = inet_incidence, eiss_incidence
                linreg_casedefs = "{casedef}", "{sm_casedef}"
                linreg_seasons = {linreg_seasons:co}
                linreg_country = {country}
        [datasets]
            [[not_ignore]]
                label = "Include all surveys"
                first_survey = 1

                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = mix
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[inet]]
                label = Ignore first survey (Default)
                first_survey = 2

                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = {inet_color}
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[eiss]]
                source_measure = eiss_incidence
                color = {eiss_color}
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


class AlwaysActive(Figure):
    """Create a comparison with other ILI source (eiss/google)"""

    def __init__(self, **args):
        # country, season, compare, casedef_id

        Figure.__init__(self, args)
        self.figname = "{base}_alwaysactive_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            legend_loc = outer right
            ncol = 1
            figsize = {figsize_double:co}
            lang = {lang}
            colors = {extra_colors:co}

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                left_ax = inet_incidence
                allow_empty = eiss_incidence,

                date_format = {month}
                xlabel = <<season:{season}>>
                grid = {grid}
                wrap = {wrap}
                plot_start = {plot_start}
                plot_end = {plot_end}

                linreg_intercept0 = {linreg_intercept0}
                linreg_sources = inet_incidence, eiss_incidence
                linreg_casedefs = "{casedef}", "{sm_casedef}"
                linreg_seasons = {linreg_seasons:co}
                linreg_country = {country}
        [datasets]
            [[alwaysactive]]
                always_active = True
                label = "Non-reporters don't have symptoms"

                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = mix
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[grace14]]
                always_active = False
                label = "Non-reporters don't have symptoms for 2 weeks"
                grace_period = 14

                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = mix
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[inet]]
                label = "Non-reporters are unknown (Default)"
                always_active = False

                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = {inet_color}
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[eiss]]
                source_measure = eiss_incidence
                color = {eiss_color}
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


class MinSurveys(Figure):
    """Create a comparison with other ILI source (eiss/google)"""

    def __init__(self, **args):
        # country, season, compare, casedef_id

        Figure.__init__(self, args)
        self.figname = "{base}_minsurveys_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            legend_loc = outer right
            ncol = 1
            figsize = {figsize_double:co}
            lang = {lang}
            colors = {extra_colors:co}
            subtitle = <<website_extra:minsurveys>> <<extra:and>>

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                left_ax = inet_incidence
                allow_empty = eiss_incidence,

                date_format = {month}
                xlabel = <<season:{season}>>
                grid = {grid}
                wrap = {wrap}
                plot_start = {plot_start}
                plot_end = {plot_end}

                linreg_intercept0 = {linreg_intercept0}
                linreg_sources = inet_incidence, eiss_incidence
                linreg_casedefs = "{casedef}", "{sm_casedef}"
                linreg_seasons = {linreg_seasons:co}
                linreg_country = {country}
        [datasets]
            [[min1]]
                min_surveys = 1
                label = "Include everybody"

                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = mix
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[inet]]
                label = At least 3 surveys (Default)
                min_surveys = 3

                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = {inet_color}
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[min5]]
                min_surveys = 5
                label = "At least 5 surveys"

                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = mix
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[eiss]]
                source_measure = eiss_incidence
                color = {eiss_color}
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


class MaxFreq(Figure):
    """Create a comparison with other ILI source (eiss/google)"""

    def __init__(self, **args):
        # country, season, compare, casedef_id

        Figure.__init__(self, args)
        self.figname = "{base}_maxfreq_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            legend_loc = outer right
            ncol = 1
            figsize = {figsize_double:co}
            lang = {lang}
            colors = {extra_colors:co}

            url = {url}
            date = {date}
            logo = {logo}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                left_ax = inet_incidence
                allow_empty = eiss_incidence,

                date_format = {month}
                xlabel = <<season:{season}>>
                grid = {grid}
                wrap = {wrap}
                plot_start = {plot_start}
                plot_end = {plot_end}

                linreg_intercept0 = {linreg_intercept0}
                linreg_sources = inet_incidence, eiss_incidence
                linreg_casedefs = "{casedef}", "{sm_casedef}"
                linreg_seasons = {linreg_seasons:co}
                linreg_country = {country}
        [datasets]
            [[freqall]]
                label = "Include everybody"
                max_freq = 0

                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = mix
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[inet]]
                label = "Report every 3 weeks (Default)"
                max_freq = 20

                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = {inet_color}
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[freq14]]
                label = "Report every 2 weeks"
                max_freq = 13

                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = mix
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[eiss]]
                source_measure = eiss_incidence
                color = {eiss_color}
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
