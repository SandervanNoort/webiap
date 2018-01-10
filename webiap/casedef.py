#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2013 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Various case definitions"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import iap

from .figure import Figure


def Casedef(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if "@" in args["casedef_id"]:
        if "s800" in args["casedef_id"]:
            yield Casedef2Venn(**args)
        else:
            if args["season"] == "all":
                yield Casedef2All(**args)
            else:
                yield Casedef2Season(**args)

    elif args["season"] == "all":
        yield CasedefAllYear(**args)
        yield CasedefAllMonth(**args)
    else:
        yield CasedefSeason(**args)
        if args["casedef_id"].startswith("ili"):
            yield CasedefSeasonBase(**args)


class Casedef2Season(Figure):
    """Compare 2 casedefs"""

    def __init__(self, **args):
        Figure.__init__(self, args)
        self.figname = "{base}_compare_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize:co}

            title_labels = measure,casedef
            legend_labels = casedef,

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                ymin = 0

                date_format = {month}
                xlabel = <<season:{season}>>
                grid = {grid}
                wrap = {wrap}
                plot_start = {plot_start}
                plot_end = {plot_end}
                {ymax_line}
        [datasets]
            [[casedef1]]
                source_measure = inet_incidence

                daily = {inet_daily}
                country = {country}
                subset = {subset}
                season = {season}
                color = {inet_color}
                band_color = {inet_band}
                linewidth = {inet_lw}
                min_participants = {min_participants}
                casedef = {casedef1}
                casedef_id = {casedef1_id}
                marker = {inet_marker}
                markersize = {markersize}
                # ax_name = inet_incidence::<<casedef:{casedef1_id}>>
                reload = {reload}
            [[casedef2]]
                source_measure = inet_incidence

                daily = {inet_daily}
                country = {country}
                subset = {subset}
                season = {season}
                color = {inet2_color}
                band_color = {inet2_band}
                linewidth = {inet_lw}
                min_participants = {min_participants}
                casedef = {casedef2}
                casedef_id = {casedef2_id}
                marker = {inet_marker}
                markersize = {markersize}
                # ax_name = inet_incidence::<<casedef:{casedef2_id}>>
                reload = {reload}
        """


class Casedef2All(Figure):
    """Compare 2 casedefs"""

    def __init__(self, **args):
        Figure.__init__(self, args)
        self.figname = "{base}_compare_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize_double:co}

            title_labels = measure,casedef
            ignore_labels = season,

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                date_format = year
                ymin = 0

                grid = {grid}
                wrap = {wrap}
                {ymax_line}
        [datasets]
            [[casedef1]]
                source_measure = inet_incidence

                daily = {year_daily}
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                color = {inet_color}
                linewidth = {year_lw}
                min_participants = {min_participants}
                casedef = {casedef1}
                casedef_id = {casedef1_id}
                # ax_name = inet_incidence::<<casedef:{casedef1_id}>>
                reload = {reload}
            [[casedef2]]
                source_measure = inet_incidence

                daily = {year_daily}
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                color = {inet2_color}
                band_color = {inet2_band}
                linewidth = {year_lw}
                min_participants = {min_participants}
                casedef = {casedef2}
                casedef_id = {casedef2_id}
                # ax_name = inet_incidence::<<casedef:{casedef2_id}>>
                reload = {reload}
        """


class Casedef2Venn(Figure):
    """Compare 2 casedefs, with Venn diagram"""

    def __init__(self, **args):
        # country, season, compare, casedef_id

        Figure.__init__(self, args)
        if args["season"] == "all":
            return

        self.figname = "{base}_venn_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize_double:co}
            lang = {lang}
            cols = 3, 2

            title_labels = casedef,
            datasets = self,casedef

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[inet_self]]
                col = 0
                left_ax = inet_incidence::<<casedef:{casedef1_id}>>
                ymin = 0
                ymin2 = 0

                date_format = {month}
                grid = {grid}
                wrap = {wrap}
                plot_start = {plot_start}
                plot_end = {plot_end}
                datasets = self, casedef
            [[venn]]
                col = 1
                type = venn
                datasets = self,casedef,overlap,all
        [datasets]
            [[self]]
                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                color = {self_color}
                min_participants = {min_participants}
                linewidth = {inet_lw}
                casedef = {casedef1}
                casedef_id = {casedef1_id}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                ax_name = inet_incidence::<<casedef:{casedef1_id}>>
                reload = {reload}
            [[casedef]]
                source_measure = inet_incidence
                country = {country}
                subset = {subset}
                season = {season}
                min_participants = {min_participants}
                linewidth = {inet_lw}
                daily = {inet_daily}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
                color = {inet_color}
                casedef = {casedef2}
                casedef_id = {casedef2_id}
                ax_name = inet_incidence::<<casedef:{casedef2_id}>>
            [[overlap]]
                source_measure = inet_incidence
                season = {season}
                country = {country}
                subset = {subset}
                daily = {inet_daily}
                reload = {reload}
                casedef = {casedef1} AND {casedef2}
                casedef_label = overla
            [[all]]
                source_measure = inet_surveys
                country = {country}
                subset = {subset}
                season = {season}
                reload = {reload}
        """


class CasedefSeasonBase(Figure):
    """Casedef in comparison with previous season"""

    def __init__(self, **args):
        # country, season, casedef_id

        Figure.__init__(self, args)

        self.figname = "{base}_base_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize:co}

            legend_labels = casedef,
            title_labels = casedef,

            logo = {logo}
            url = {url}
            date = {date}
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
                xlabel = <<season:{season}>>
                datasets = current,
                baseline = baseline,
                baseline_min = {baseline_min}
                {ymax_line}
        [datasets]
            [[current]]
                source_measure = inet_incidence
                daily = {inet_daily}
                country = {country}
                subset = {subset}
                season = {season}
                color = {inet_color}
                band_color = {inet_band}
                linewidth = {inet_lw}
                min_participants = {min_participants}
                casedef = {casedef}
                casedef_id = {casedef_id}
                marker = {inet_marker}
                markersize = {markersize}
                min_surveys = {min_surveys}
                reload = {reload}
            [[baseline]]
                source_measure = inet_incidence
                country = {country}
                subset = {subset}
                season_values = {linreg_seasons:co}
                casedef = {casedef}
                casedef_id = {casedef_id}
                samples_onsets = {samples_threshold}
                color = {baseline_color}
                linewidth = {baseline_width}
        """

    def set_params(self):
        Figure.set_params(self)
        self.params["season_prev"] = iap.utils.prev_season(
            self.params["season"])

    def test(self, ini):
        if not Figure.test(self, ini):
            return False
        if self.params["season"] not in [
                options["season"] for options in ini.datasets.values()]:
            self.done("No current season")
            return False

        datadict = iap.Data(ini.datasets["current"]).get_datadict()
        if sum([values["inet_incidence"] for values in datadict.values()
                if "inet_incidence" in values]) == 0:
            self.done("Empty current season")
            return False
        return True


class CasedefSeason(Figure):
    """Casedef in comparison with previous season"""

    def __init__(self, **args):
        # country, season, casedef_id

        Figure.__init__(self, args)

        self.figname = "{base}_prev_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize:co}

            legend_labels = season,

            logo = {logo}
            url = {url}
            date = {date}
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
                {ymax_line}
        [datasets]
            [[previous]]
                source_measure = inet_incidence

                daily = {inet_daily}
                country = {country}
                subset = {subset}
                season = {season_prev}
                color = {inet2_color}
                band_color = {inet2_band}
                linewidth = {inet_lw}
                min_participants = {min_participants}
                casedef = {casedef}
                casedef_id = {casedef_id}
                marker = {inet_marker}
                markersize = {markersize}
                min_surveys = {min_surveys}
                reload = {reload}
            [[current]]
                source_measure = inet_incidence

                daily = {inet_daily}
                country = {country}
                subset = {subset}
                season = {season}
                color = {inet_color}
                band_color = {inet_band}
                linewidth = {inet_lw}
                min_participants = {min_participants}
                casedef = {casedef}
                casedef_id = {casedef_id}
                marker = {inet_marker}
                markersize = {markersize}
                min_surveys = {min_surveys}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)
        self.params["season_prev"] = iap.utils.prev_season(
            self.params["season"])

    def test(self, ini):
        if not Figure.test(self, ini):
            return False
        if self.params["season"] not in [
                options["season"] for options in ini.datasets.values()]:
            self.done("No current season")
            return False

        datadict = iap.Data(ini.datasets["current"]).get_datadict()
        if sum([values["inet_incidence"] for values in datadict.values()
                if "inet_incidence" in values]) == 0:
            self.done("Empty current season")
            return False
        return True


def Reporting(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    yield ReportingSeason(**args)
    if args["country"] == "nl":
        yield ReportingSeason(extra_countries="be,", **args)


class ReportingSeason(Figure):
    """Casedef in comparison with previous season"""

    def __init__(self, **args):
        # country, season, casedef_id

        Figure.__init__(self, args)

        if args["season"] == "all":
            return

        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize:co}

            legend_labels = season,

            logo = {logo}
            url = {url}
            date = {date}
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
                source_measure = inet_reporting
                ignore_first = False
                ignore_double = False
                min_surveys = {min_surveys}
                onset = survey

                daily = {inet_daily}
                country = {country}
                subset = {subset}
                season = {season_prev}
                color = {inet_prev}
                linewidth = {inet_lw}
                min_participants = {min_participants}
                casedef = {casedef}
                casedef_id = {casedef_id}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
            [[current]]
                source_measure = inet_reporting
                ignore_first = False
                ignore_double = False
                min_surveys = {min_surveys}
                onset = survey
                max_freq         = 0

                daily = {inet_daily}
                country = {country}
                subset = {subset}
                season = {season}
                color = {inet_color}
                linewidth = {inet_lw}
                min_participants = {min_participants}
                casedef = {casedef}
                casedef_id = {casedef_id}
                marker = {inet_marker}
                markersize = {markersize}
                reload = {reload}
        """

        self.figname = "{base}_reporting_{casedef_id}{size_ext}"

    def set_params(self):
        Figure.set_params(self)
        self.params["season_prev"] = iap.utils.prev_season(
            self.params["season"])

    def test(self, ini):
        if not Figure.test(self, ini):
            return False
        if self.params["season"] not in [
                options["season"] for options in ini.datasets.values()]:
            self.done("No current season")
            return False

        datadict = iap.Data(ini.datasets["current"]).get_datadict()
        if sum([values["inet_reporting"] for values in datadict.values()
                if "inet_reporting" in values]) == 0:
            self.done("Empty current season")
            return False
        return True


class CasedefAllMonth(Figure):
    """Create a comparison with other sources"""

    def __init__(self, **args):
        # country, casedef_id
        Figure.__init__(self, args)

        self.figname = "{base}_month_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            figsize = {figsize_double:co}
            legend_loc = {legend_loc_all}
            ncol = {ncol_all}

            legend_labels = {legend_labels}
            title_labels = {title_labels}

            logo = {logo}
            url = {url}
            date = {date}
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
                datasets = default,
                baseline = {baseline}
                {ymax_line}
        [datasets]
            [[default]]
                source_measure = inet_incidence
                color = mix

                daily = {year_daily}
                country = {country}
                subset = {subset}
                season_values = {seasons_reversed:co}
                min_participants = {min_participants}
                linewidth = {month_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                reload = {reload}
            [[baseline]]
                source_measure = inet_incidence
                country = {country}
                subset = {subset}
                season_values = {linreg_seasons:co}
                casedef = {casedef}
                casedef_id = {casedef_id}
                samples_onsets = {samples_threshold}
                color = {baseline_color}
                linewidth = {baseline_width}
        """

    def set_params(self):
        Figure.set_params(self)
        if self.params["size"] == "big":
            self.params["right_ncol"] = 1
        else:
            self.params["right_ncol"] = 2

        if self.params["casedef_id"].startswith("ili"):
            self.params["baseline"] = "baseline,"
            self.params["legend_labels"] = ","
            self.params["title_labels"] = "casedef,"
        else:
            self.params["baseline"] = ","
            self.params["legend_labels"] = ","
            self.params["title_labels"] = ","


class CasedefAllYear(Figure):
    """Create a comparison with other sources"""

    def __init__(self, **args):
        # country, casedef_id
        Figure.__init__(self, args)
        self.figname = "{base}_year_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            figsize = {figsize_double:co}
            legend_loc = {legend_loc}
            ncol = 0

            ignore_labels = season,
            legend_labels = {legend_labels}
            title_labels = {title_labels}

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot]]
                date_format = year
                ymin = 0

                grid = {grid}
                wrap = {wrap}
                {ymax_line}
                datasets = default,
                baseline = {baseline}
                baseline_min = {baseline_min}
        [datasets]
            [[default]]
                source_measure = inet_incidence
                daily = {year_daily}
                color = {inet_color}
                band_color = {inet_band}
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                min_participants = {min_participants}
                linewidth = {year_lw}
                casedef = {casedef}
                casedef_id = {casedef_id}
                reload = {reload}
            [[baseline]]
                source_measure = inet_incidence
                country = {country}
                subset = {subset}
                season_values = {linreg_seasons:co}
                casedef = {casedef}
                casedef_id = {casedef_id}
                samples_onsets = {samples_threshold}
                color = {baseline_color}
                linewidth = {baseline_year_width}
        """

    def set_params(self):
        Figure.set_params(self)

        if self.params["casedef_id"].startswith("ili"):
            self.params["baseline"] = "baseline,"
            self.params["legend_labels"] = "casedef,"
            self.params["title_labels"] = "casedef,"
        else:
            self.params["baseline"] = ","
            self.params["legend_labels"] = ","
            self.params["title_labels"] = ","


class Symptoms(Figure):
    """All symptoms a participant has fitting a certain casedef"""

    def __init__(self, **args):
        # country, season, casedef_id
        Figure.__init__(self, args)
        if "all" in args["season"]:
            return

        self.figname = "{base}_symptoms_{casedef_id}{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            legend_loc = {legend_loc}
            ncol = {ncol}
            figsize = {figsize_triple:co}

            subtitle = "symptoms"

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[bar]]
                type = barplot
                bars = control
                grid = {grid}
                wrap = {wrap}
                horizontal = True
                citylabels = True
                all_houses = True
                errors = {errors}
                city_zero_nominator = False
                house_zero_nominator = False
                ymax = 100
                city_sort = True
        [datasets]
            [[control1]]
                source_measure = inet_control
                country = {country}
                subset = {subset}
                season = {season}
                casedef = {casedef}
                casedef_id = {casedef_id}
                control_values = {symptoms}
                control_days = {symptoms_control_days}
                control_ids = {symptom_ids}
                control_labels = {symptom_labels}
        """

    def set_params(self):
        Figure.set_params(self)

        casedefs = []
        casedef_labels = []
        casedef_ids = []
        for answer in range(1, 19):
            casedefs.append("s100_{0}=1".format(answer))
            casedef_ids.append("s100_{0}".format(answer))
            casedef_labels.append("''")
        casedefs.append("s200>=380")
        casedef_ids.append("''")
        casedef_labels.append(">=38 C")

        casedefs.append("s220_1=1")
        casedef_ids.append("s220_1")
        casedef_labels.append("''")

        casedefs.append("s120_1=1")
        casedef_ids.append("s120_1")
        casedef_labels.append("''")

        casedefs.append(self.get_casedef("gp")[0])
        casedef_ids.append("gp")
        casedef_labels.append("''")

        casedefs.append(self.get_casedef("home")[0])
        casedef_ids.append("home")
        casedef_labels.append("''")

        self.params["symptoms"] = ",".join(casedefs)
        self.params["symptom_ids"] = ",".join(casedef_ids)
        self.params["symptom_labels"] = ",".join(casedef_labels)
