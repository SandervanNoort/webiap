#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2013 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""CSV Files"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import os
import copy
import io

import iap

from .figure import Figure
from . import config, tools


class Weeks(Figure):
    """Csv file per week"""

    def __init__(self, **args):
        Figure.__init__(self, args)

        if args["season"] == "all":
            return None

        self.figname = ("{country}_" + "_".join(
            self.params["week_casedef_list"] +
            self.params["week_cutter_list"]))
        self.inistring = """
        [plots]
            [[plot]]
                type = weeks
        [datasets]
            [[actives]]
                source_measure = inet_actives
                daily = False
                min_participants = {min_participants}
                label = Participant-weeks

                country = {country}
                subset = {subset}
                season = {season}
                cutter = {week_cutter}
                reload = {reload}
            """

    def make_fig(self, _myini):
        """No figure"""
        return True

    def set_params(self):
        Figure.set_params(self)
        self.params["week_cutter"] = "__".join(self.params["week_cutter_list"])
        for self.params["casedef_id"] in self.params["week_casedef_list"]:
            self.params["casedef"] = self.get_casedef(
                self.params["casedef_id"])[0]
            self.params["casedef_label"] = "<<casedef:{casedef_id}>>".format(
                **self.params)
            self.exclude_periods = tools.SetList()
            self.set_exclude_periods()
            self.inistring += """[[{casedef_label}]]
                source_measure = inet_cases
                daily = False
                min_participants = 0

                country = {{country}}
                subset = {subset}
                season = {{season}}
                casedef = {casedef}
                casedef_id = {casedef_id}
                label = {casedef_label}
                cutter = {{week_cutter}}
                """.format(**self.params)
        self.exclude_periods = tools.SetList()
        # del(self.params["casedef_id"])

    def make_csv(self, myini):
        """Write csv with external"""
        fname = os.path.join(self.get_dir("csv"), self.figname)
        myexport = iap.Export(myini)
        myexport.write_csv(fname, onefile=False)


class Csv(Figure):
    """Create a CSV file for all ILIe/ILIt data"""

    def __init__(self, **args):
        # country

        Figure.__init__(self, args)

        self.figname = "{base}"

        self.inistring = """
        [plots]
            [[plot]]
                type = plot
        [datasets]
            [[actives]]
                source_measure = inet_actives
                daily = False
                min_participants = 0
                label = Participant-weeks

                country = {country}
                subset = {subset}
                season_values = {seasons:co}
                reload = {reload}
            """

    def make_csv(self, myini):
        """Write csv with external"""
        fname = os.path.join(self.get_dir("csv"),
                             "{0}.csv".format(self.figname))
        tools.create_dir(fname)
        with tools.csvopen(fname, "w") as csvobj:
            fobj = io.open(os.path.join(config.CONFIG_DIR, "csv.txt"), "r")
            csvobj.write(fobj.read() + "\n\n")
            fobj.close()
            export = iap.Export(myini)
            export.write_csv(csvobj)

    def make_fig(self, _myini):
        """No figure"""
        return True

    def set_params(self):
        Figure.set_params(self)
        params = copy.deepcopy(self.params)
        for (casedef_id, label) in zip(
                config.DIAGRAMS["params"]["csv_casedefs"],
                config.DIAGRAMS["params"]["csv_headers"]):
            self.exclude_periods = tools.SetList()

            self.params["casedef_id"] = casedef_id
            self.set_exclude_periods()
            self.inistring += tools.Format("""[[{label}]]
                source_measure = inet_cases
                daily = False
                min_participants = 0

                country = {{country}}
                subset = {subset}
                season_values = {seasons:co}
                casedef = {casedef}
                label = {label}
                """).format(casedef=config.DIAGRAMS["casedefs"][casedef_id][0],
                            label=label,
                            **self.params)
        self.exclude_periods = tools.SetList()
        self.params = params
