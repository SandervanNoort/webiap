#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2013 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Participation plots"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

from .figure import Figure


def Activity(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    activity = args["activity"]
    return (Hist(**args) if activity == "hist" else
            HistTotal(**args) if activity == "hist_total" else
            Active(**args) if activity == "actives" else
            Surveys(**args) if activity == "surveys" else
            Participant(**args) if activity == "participants" else
            Days(**args) if activity == "days" else
            Frequency(**args) if activity == "freq" else
            None)


def Active(**args):
    """Active factory"""
    # (Invalid name) pylint: disable=C0103
    if args["season"] == "all":
        return ActiveAll(**args)
    else:
        return ActiveSeason(**args)


class ActiveSeason(Figure):
    """Number of active participants in time (one season)"""

    def __init__(self, **args):
        # country, season

        Figure.__init__(self, args)
        self.figname = "{base}_part_actives{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            figsize = {figsize:co}
            legend_loc = {legend_loc}
            ncol = {ncol}

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot_actives]]
                ymin = 0

                date_format = {month}
                xlabel = <<season:{season}>>
                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[actives]]
                source_measure = inet_actives
                country = {country}
                subset = {subset}
                season = {season}
                min_surveys = {min_surveys}

                daily = True
                min_value = {min_value}
                limits = dotted
                linewidth = {lw}
                color = {participants_color}
                reload = {reload}
        """


class ActiveAll(Figure):
    """Number of active participants in time (all seasons)"""

    def __init__(self, **args):
        # country

        Figure.__init__(self, args)
        self.figname = "{base}_part_actives{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            figsize = {figsize_double:co}
            legend_loc = {legend_loc}
            ncol = {ncol}

            ignore_labels = season,

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot_actives]]
                date_format = year
                ymin = 0

                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[actives]]
                source_measure = inet_actives
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                min_surveys = {min_surveys}

                daily = True
                min_value = {min_value}
                limits = dotted
                linewidth = {lw}
                color = {participants_color}
                reload = {reload}
        """


def Participant(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        return ParticipantAll(**args)
    else:
        return ParticipantSeason(**args)


class ParticipantSeason(Figure):
    """Active participants and surveys"""

    def __init__(self, **args):
        # country, season

        Figure.__init__(self, args)

        self.figname = "{base}_part_participants{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            lang = {lang}
            figsize = {figsize:co}
            legend_loc = {legend_loc}
            ncol = {ncol}

            city_cutter_label = <<measure:participants>>

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot_activity]]
                left_ax = inet_participants
                linreg_gradient = 1
                linreg_intercept = 0
                linreg_sources = inet_participants, inet_surveys
                ymin = 0

                date_format = {month}
                xlabel = <<season:{season}>>
                grid = {grid}
                wrap = {wrap}
                yticks = {yticks}
                yticks2 = {yticks}

        [datasets]
            [[participants]]
                source_measure = inet_participants
                country = {country}
                season = {season}
                subset = {subset}
                min_surveys = 0  # all participants

                daily = True
                linewidth = {lw}
                color = {participants_color}
                reload = {reload}
            [[surveys]]
                source_measure = inet_surveys
                country = {country}
                subset = {subset}
                season = {season}
                min_surveys = 0  # all surveys

                daily = False
                min_value = {min_value}
                xmaster = True
                bar = True
                color = {surveys_color}
                reload = {reload}
        """


class ParticipantAll(Figure):
    """All participants per season with more/less 3 surveys"""

    def __init__(self, **args):
        # country

        Figure.__init__(self, args)
        self.figname = "{base}_part_participants{size_ext}"
        self.inistring = r"""
        [fig]
            title = auto
            lang = {lang}
            figsize = {figsize:co}
            legend_loc = {legend_loc}
            ncol = {ncol}

            city_labels = season,
            legend_labels = season,
            short = True

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot_hist]]
                type = barplot
                bars = absolute
                xlabel_id = season
                floors = True

                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[inet]]
                source_measure = inet_participants
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                min_surveys = {min_surveys}

                label = ">={min_surveys} <<extra:surveys>>"
                color = {participants_color}
                reload = {reload}
            [[inet2]]
                source_measure = inet_participants
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                intake = "surveys<'{min_surveys}'"
                min_surveys = 0  # non-active participants

                label = "<{min_surveys} <<extra:surveys>>"
                color = {nonactive_color}
                reload = {reload}
        """


def Surveys(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        return SurveysAll(**args)
    else:
        return SurveysSeason(**args)


class SurveysSeason(Figure):
    """Number of completed surveys"""

    def __init__(self, **args):
        # country, season

        Figure.__init__(self, args)
        self.figname = "{base}_part_completed{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            ax_margins_extra = 0, 0, 20, 0
            lang = {lang}
            figsize = {figsize:co}
            legend_loc = {legend_loc}
            ncol = {ncol}

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot_days]]
                type = barplot
                bars = absolute
                answer_group = city
                housedistance = {housedistance}
                floors = True
                xlabel_id = surveys
                all_cities = True

                xangle = {xangle}
                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[inet]]
                source_measure = inet_participants
                country = {country}
                subset = {subset}
                season = {season}
                min_surveys = 0  # show also with few surveys
                city_cutter = {surveys_distribution}

                city_cutter_label = <<xlabel:surveys>>
                color = {participants_color}
                reload = {reload}
        """


class SurveysAll(Figure):
    """Average completed surveys per week for each season"""

    def __init__(self, **args):
        # country

        Figure.__init__(self, args)
        self.figname = "{base}_part_surveys{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            ax_margins_extra = 0, 0, 20, 0

            lang = {lang}
            figsize = {figsize:co}
            legend_loc = {legend_loc}
            ncol = {ncol}

            city_labels = season,
            legend_labels = season,
            short = True

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot_surveys]]
                type = barplot
                bars = surveys
                xlabel_id = season

                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[inet]]
                source_measure = inet_surveys
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                min_surveys = 0  # completed surveys per week

                color = {surveys_color}
                reload = {reload}
        """


def Days(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        return None
    else:
        return DaysSeason(**args)


class DaysSeason(Figure):
    """Number of days a participants active"""

    def __init__(self, **args):
        # country, season

        Figure.__init__(self, args)
        self.figname = "{base}_part_days{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            ax_margins_extra = 0, 0, 30, 0

            lang = {lang}
            figsize = {figsize:co}
            legend_loc = {legend_loc}
            ncol = {ncol}

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot_days]]
                type = barplot
                bars = absolute
                answer_group = city
                housedistance = {housedistance}
                floors = True
                xlabel_id = days
                all_cities = True

                xangle = {xangle}
                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[inet]]
                source_measure = inet_participants
                country = {country}
                subset = {subset}
                season = {season}
                min_surveys = {min_surveys}
                city_cutter = {days_distribution}

                color = {participants_color}
                reload = {reload}
        """


def Frequency(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        return None
    else:
        return FrequencySeason(**args)


class FrequencySeason(Figure):
    """Average number of days between two surveys"""

    def __init__(self, **args):
        # country, season

        Figure.__init__(self, args)
        self.figname = "{base}_part_freq{size_ext}"
        self.inistring = """
        [fig]
            title = auto
            ax_margins_extra = 0, 0, 20, 0

            lang = {lang}
            figsize = {figsize:co}
            legend_loc = {legend_loc}
            ncol = {ncol}

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot_days]]
                type = barplot
                bars = absolute
                answer_group = city
                housedistance = {housedistance}
                floors = True
                xlabel_id = freq
                all_cities = True

                xangle = {xangle}
                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[inet]]
                source_measure = inet_participants
                country = {country}
                subset = {subset}
                season = {season}
                city_cutter = {freq_distribution}
                min_surveys = {min_surveys}

                color = {participants_color}
                reload = {reload}
        """


def Hist(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        return HistAll(**args)
    else:
        return HistSeason(**args)


class HistSeason(Figure):
    """Histogram of the participants age distribution compared to population"""

    def __init__(self, **args):
        # country, season

        Figure.__init__(self, args)
        self.figname = "{base}_part_hist_perc{size_ext}"
        self.inistring = """
        [fig]
            title = auto

            lang = {lang}
            figsize = {figsize:co}
            legend_loc = {legend_loc}
            ncol = {ncol}
            {age_format}

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot_hist]]
                type = barplot
                bars = percentage_by_label
                answer_group = city
                housedistance = {housedistance}
                xlabel_id = age_group

                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[inet]]
                source_measure = inet_participants
                country = {country}
                subset = {subset}
                season = {season}
                city_cutter = {age_distribution}
                min_surveys = {min_surveys}

                color = {inet_color}
                reload = {reload}
            [[eiss]]
                source_measure = europe_participants
                country = {country}
                subset = {subset}
                season = {season}
                city_cutter = {age_distribution}

                color = {eiss_color}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if "inet" not in [options["source"]
                          for options in myini.datasets.values()]:
            self.done("No draw")
            return False
        return True


class HistAll(Figure):
    """Histogram of the participants age distribution compared to population
            all seasons"""

    def __init__(self, **args):
        # country

        Figure.__init__(self, args)
        self.figname = "{base}_part_hist_perc{size_ext}"
        self.inistring = """
        [fig]
            title = auto

            legend_loc = {legend_loc_all}
            ncol = {ncol_all}
            lang = {lang}
            figsize = {figsize_double:co}

            legend_labels = season,
            ignore_labels = source,
            {age_format}

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot_hist]]
                type = barplot
                bars = percentage_by_label
                answer_group = city
                housedistance = {housedistance}
                xlabel_id = age_group

                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[inet]]
                source_measure = inet_participants
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                city_cutter = {age_distribution}
                min_surveys = {min_surveys}

                color = mix
                reload = {reload}
            [[eiss]]
                source_measure = europe_participants
                country = {country}
                subset = {subset}
                city_cutter = {age_distribution}

                label = <<source:europe>>
                color = {population_color}
                reload = {reload}
        """

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if "inet" not in [options["source"]
                          for options in myini.datasets.values()]:
            self.done("No draw")
            return False
        return True


def HistTotal(**args):
    """Factory function"""
    # (Invalid name) pylint: disable=C0103

    if args["season"] == "all":
        return HistTotalAll(**args)
    else:
        return HistTotalSeason(**args)


class HistTotalSeason(Figure):
    """Histogram of the all participants age groups (absolute numbers)"""

    def __init__(self, **args):
        # country, season

        Figure.__init__(self, args)
        self.figname = "{base}_part_hist_total{size_ext}"
        self.inistring = r"""
        [fig]
            title = auto

            lang = {lang}
            figsize = {figsize:co}
            legend_loc = {legend_loc}
            ncol = {ncol}
            {age_format}

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot_hist]]
                type = barplot
                bars = absolute
                answer_group = city
                housedistance = {housedistance}
                floors = True
                xlabel_id = age_group

                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[inet]]
                source_measure = inet_participants
                country = {country}
                subset = {subset}
                season = {season}
                city_cutter = {age_distribution}
                min_surveys = {min_surveys}

                color = {participants_color}
                label = ">={min_surveys} <<extra:surveys>>"
                reload = {reload}
            [[inet2]]
                source_measure = inet_participants
                country = {country}
                subset = {subset}
                season = {season}
                intake = "surveys<'{min_surveys}'"
                city_cutter = {age_distribution}
                min_surveys = 0  # inactive participants

                label = "<{min_surveys} <<extra:surveys>>"
                color = {nonactive_color}
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if "inet" not in [options["source"]
                          for options in myini.datasets.values()]:
            self.done("No draw")
            return False
        return True


class HistTotalAll(Figure):
    """Histogram of the all participants age groups (absolute numbers)"""

    def __init__(self, **args):
        Figure.__init__(self, args)

        self.figname = "{base}_part_hist_total{size_ext}"
        self.inistring = """
        [fig]
            title = auto

            lang = {lang}
            figsize = {figsize_double:co}
            legend_loc = {legend_loc_all}
            ncol = {ncol_all}

            ignore_labels = measure,
            legend_labels = season,
            {age_format}

            logo = {logo}
            url = {url}
            date = {date}
            [[rc]]
                font.family = {font}
                legend.fontsize = {legend}
        [plots]
            [[plot_hist]]
                type = barplot
                bars = absolute
                answer_group = city
                housedistance = {housedistance}
                xlabel_id = age_group

                grid = {grid}
                wrap = {wrap}
        [datasets]
            [[inet]]
                source_measure = inet_participants
                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                city_cutter = {age_distribution}
                min_surveys = {min_surveys}

                color = mix
                reload = {reload}
        """

    def set_params(self):
        Figure.set_params(self)

    def test(self, myini):
        if not Figure.test(self, myini):
            return False
        if "inet" not in [options["source"]
                          for options in myini.datasets.values()]:
            self.done("No draw")
            return False
        return True
