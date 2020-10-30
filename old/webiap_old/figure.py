#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2013 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Basic class for all result diagrams"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import os
import time

import iap.fig

from . import config, tools


class Figure(object):
    """Basic class for generating results ini/png/csv"""

    def __init__(self, params=None):
        self.params = params
        self.figname = ""
        self.inistring = ""
        self.exclude_periods = tools.SetList()
        self.msg = "DONE"

        self.time0 = time.time()

    def done(self, msg):
        """Set the result msg"""
        self.msg = msg

    def get_dir(self, ftype):
        """Return language specific dirname"""
        if "lang" in self.params:
            return config.get_dir(ftype, self.params["lang"])
        else:
            return config.get_dir(ftype)

    def test(self, ini):
        """Test if there are enough datasets"""

        for options in ini.datasets.values():
            if ("cutter" in options and
                    "region" in options["cutter"] and
                    options["subset"] != ""):
                self.done("Subset: {subset}, cutter: {cutter}".format(
                    **options))
                return False

        # remove inet datasets in excluded periods
        for plotname, options in ini.datasets.items():
            if options["source"] == "inet" \
                    and options["period"] in self.exclude_periods:
                del ini.datasets[plotname]

        if len(ini.datasets.keys()) == 0:
            self.msg = "No datasets"
            return False
        return True

    @staticmethod
    def get_casedef(casedef_id):
        """Return the casedef if defined"""
        if casedef_id in config.DIAGRAMS["casedefs"]:
            return config.DIAGRAMS["casedefs"][casedef_id]
        else:
            return casedef_id, 0

    def set_params(self):
        """Set the params"""
        self.params.update(config.DIAGRAMS["ini"])

        self.params["base"] = "{region}_{year}".format(
            region=(self.params["subset"] if "subset" in self.params and
                    self.params["subset"] != "" else
                    self.params["country"]),
            year=("none" if "season" not in self.params else
                  "all" if self.params["season"] == "all" else
                  iap.utils.season_to_years(self.params["season"])[0]))

        if "subset" in self.params and self.params["subset"] != "":
            self.params["subset"] = config.DIAGRAMS["subset"][
                self.params["subset"]]

        if "size" in self.params and self.params["size"] == "big":
            self.params["size_ext"] = "_big"
            self.params.update(config.DIAGRAMS["ini_big"])
        else:
            self.params["size_ext"] = ""

        if "casedef_id" in self.params:
            if "@" in self.params["casedef_id"]:
                self.params["casedef1_id"], self.params["casedef2_id"] = \
                    self.params["casedef_id"].split("@")
                self.params["casedef1"], ymax = self.get_casedef(
                    self.params["casedef1_id"])
                self.params["ymax_line"] = (
                    "ymax = {0}".format(ymax)
                    if float(ymax) > 0 and False else
                    "")
                self.params["casedef2"], ymax = self.get_casedef(
                    self.params["casedef2_id"])
                self.params["ymax2_line"] = (
                    "ymax2 = {0}".format(ymax)
                    if float(ymax) > 0 and False else
                    "")
            else:
                self.params["casedef"], ymax = self.get_casedef(
                    self.params["casedef_id"])
                self.params["ymax_line"] = (
                    "ymax = {0}".format(ymax) if float(ymax) > 0 else
                    "")

        if "control_id" in self.params:
            self.params["control"] = self.get_casedef(
                self.params["control_id"])[0]

    def set_exclude_periods(self):
        """Exclude periods for which data is not complete"""

        for param, values in config.DIAGRAMS["exclude"].items():
            for param2 in (["casedef_id", "casedef1_id", "casedef2_id"]
                           if param == "casedef_id" else
                           [param]):
                for value, periods in values.items():
                    if param2 in self.params and self.params[param2] == value:
                        self.exclude_periods.extend(periods)

        if "country" in self.params:
            self.params["seasons"] = [
                season
                for season in self.params["seasons"]
                if iap.utils.country_season_to_period(
                    self.params["country"], season)
                not in self.exclude_periods]
            self.params["linreg_seasons"] = [
                season
                for season in self.params["linreg_seasons"]
                if iap.utils.country_season_to_period(
                    self.params["country"], season)
                not in self.exclude_periods]
            self.params["seasons_reversed"] = self.params["seasons"]

    def make_fig(self, ini):
        """Create a figure"""
        fig = iap.fig.Fig(ini.settings)
        for plot_settings in ini.settings["plots"].values():
            if not iap.fig.dia(fig, plot_settings, ini.datasets).draw():
                self.msg = "No draw"
                return False
        if "map" in ini.settings and "mapname" in ini.settings["map"]:
            fig.save(os.path.join(self.get_dir("map"), self.figname))
        elif "fig" in ini.settings:
            fig.save(os.path.join(self.get_dir("png"), self.figname + ".png"))
            fig.savefig(os.path.join(self.get_dir("pdf"),
                                     self.figname + ".pdf"))
        return True

    def make_csv(self, ini):
        """Create a csv file"""
        export = iap.Export(ini, self.params["force_daily"])
        export.write_csv(os.path.join(self.get_dir("csv"), self.figname))

    def remove(self):
        """Remove file if it does not exist"""
        for ext in ["ini", "csv", "png", "pdf"]:
            fname = os.path.join(self.get_dir(ext),
                                 "{0}.{1}".format(self.figname, ext))
            if os.path.exists(fname):
                os.remove(fname)

    def setup(self):
        """Set the params and return the name"""

        if self.inistring == "":
            return None
        self.set_params()
        self.set_exclude_periods()
        self.figname = self.figname.format(**self.params)
        self.inistring = tools.Format(self.inistring).format(**self.params)
        return self.figname.format(**self.params)

    def save(self):
        """Create the png/csv/ini"""

        ini = iap.Ini(self.inistring)
        if not self.test(ini):
            self.remove()
            return self.msg

        if not self.make_fig(ini):
            self.remove()
            return self.msg

        if self.params["csv"]:
            self.make_csv(ini)

        ini.write(os.path.join(self.get_dir("ini"), self.figname))
        return self.msg
