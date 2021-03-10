#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2012 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Create all the results for web page"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import sys
import argparse
import time
import itertools
import collections
import traceback
import logging

import webiap
import iap

from webiap import tools

BOOLEANS = []


def stat_run(function, **options):
    """Run the function"""

    graphs = function(**options)
    if not isinstance(graphs, collections.Iterable):
        graphs = [graphs]

    for graph in graphs:
        if graph is None:
            continue

        figname = graph.setup()
        if figname is None:
            continue
        yield "Start: {0}".format(figname)

        try:
            result = graph.save()
            yield " Done: {0} ({1})".format(figname, result)
        except iap.IAPError as inst:
            error = traceback.format_exc() if options["do_raise"] else inst
            yield " ERROR: {0} ({1})".format(figname, error)
        except Exception as inst:
            error = traceback.format_exc() if options["do_raise"] else inst
            yield "ERROR: {0}\n{1}".format(figname, error)


class Website(object):
    """Create all results"""

    def __init__(self):
        self.cmd_options = self.get_cmd()

    def parse(self, name):
        """Parse an argument as a comma seperated list"""

        if name == "cold":
            return ["cold" + ili[3:] for ili in self.parse("ili") if ili.startswith("ili")]
        elif name == "allergy":
            return ["allergy" + ili[3:] for ili in self.parse("ili") if ili.startswith("ili")]
        elif name == "gastro":
            return ["gastro" + ili[3:] for ili in self.parse("ili") if ili.startswith("ili")]
        elif name == "":
            return []

        # a list, to not extend DIAGRAMS
        values = tools.SetList(getattr(self.cmd_options, name + "_list"))
        all_values = tools.SetList(
            webiap.config.DIAGRAMS["params"][name + "_list"])

    #     elif name == "week_casedef_list":
    #         all_values.extend(webiap_old.config.DIAGRAMS["params"]["ili_list"])
    #         all_values.extend(webiap_old.config.DIAGRAMS["params"]["cold_list"])
    #         all_values.extend(webiap_old.config.DIAGRAMS["params"]["venn_list"])
    #         all_values.extend(webiap_old.config.DIAGRAMS["params"]["casedef_list"])
    #     elif name == "week_cutter_list":
    #         all_values.extend(webiap_old.config.DIAGRAMS["params"]["cutter_list"])

        default = (webiap.config.DIAGRAMS["params"][name + "_default"]
                   if name + "_default" in webiap.config.DIAGRAMS["params"] else
                   [])

        if values is None or len(values) == 0:
            values = all_values if self.cmd_options.ALL else default
        if "help" in values:
            sys.exit(
                "Possible values for {name}:\n   {values}".format(
                    name=name, values=", ".join(all_values)))
        elif "ALL" in values:
            values = all_values
        elif "NONE" in values:
            values = []
        dif = set(values) - set(all_values)
        if not self.cmd_options.unknown and len(dif) > 0:
            sys.exit("Unknown {0}: {1}".format(name, ",".join(dif)))
        if name in BOOLEANS:
            values = [bool(int(val)) for val in values]

        if name == "syndrome":
            for syndrome in ["ili", "cold", "allergy", "gastro"]:
                if syndrome in values:
                    values.remove(syndrome)
                    values.extend(self.parse(syndrome))

        return values

    @staticmethod
    def get_parser():
        """Return the commandline parser"""
        parser = argparse.ArgumentParser()
        parser.add_argument(nargs="+", action="store", dest="times")

        parser.add_argument("-src", "--source_list", nargs="+", action="store",
                            dest="source_list")
        parser.add_argument("-cmp", "--compare_list", nargs="+",
                            action="store", dest="compare_list")
        parser.add_argument("-cut", "--cutter_list", nargs="+", action="store",
                            dest="cutter_list")
        parser.add_argument("-his", "--histogram_list", nargs="+",
                            action="store", dest="histogram_list")
        parser.add_argument("-sub", "--subset_list", nargs="+",
                            action="store", dest="subset_list")
        parser.add_argument("-avg", "--average_list", nargs="+",
                            action="store", dest="average_list")
        parser.add_argument("-ili", "--ili_list", nargs="+", action="store",
                            dest="ili_list")
        parser.add_argument("-ven", "--venn_list", nargs="+", action="store",
                            dest="venn_list")
        parser.add_argument("-syn", "--syndrome_list", nargs="+",
                            action="store", dest="syndrome_list")
        parser.add_argument("-age", "--age_list", nargs="+", action="store",
                            dest="age_list")
        parser.add_argument("-act", "--activity_list", nargs="+",
                            action="store", dest="activity_list")
        parser.add_argument("-ana", "--analysis_list", nargs="+",
                            action="store", dest="analysis_list")
        parser.add_argument("-con", "--control_list", nargs="+",
                            action="store", dest="control_list")
        parser.add_argument("-cas", "--casedef_list", nargs="+",
                            action="store", dest="casedef_list")
        parser.add_argument("-siz", "--size_list", nargs="+", action="store",
                            dest="size_list")
        parser.add_argument("-lan", "--lang_list", nargs="+", action="store",
                            dest="lang_list")
        parser.add_argument("-wca", "--week_casedef_list", nargs="+",
                            action="store", dest="week_casedef_list")
        parser.add_argument("-wcu", "--week_cutter_list", nargs="+",
                            action="store", dest="week_cutter_list")

        parser.add_argument("-csv", "--csv", action="store_true")
        parser.add_argument("-nocsv", "--no-csv", action="store_true")

        parser.add_argument("-rep", "--reporting", action="store_true",
                            default=False)

        parser.add_argument("-sym", "--symptoms", action="store_true")
        parser.add_argument("-nosym", "--no-symptoms", action="store_true")

        parser.add_argument("-map", "--maps", action="store_true",
                            default=False)
        parser.add_argument("-rel", "--reload", action="store_true",
                            default=False)
        parser.add_argument("-deb", "--debug", action="store", dest="debug",
                            default="error")
        parser.add_argument("-unk", "--unknown", action="store_true",
                            default=False, dest="unknown")
        parser.add_argument("-rai", "--raise", action="store_true",
                            default=False, dest="do_raise")

        parser.add_argument("-cpu", "--cpus", action="store", dest="cpus")
        parser.add_argument("-ALL", action="store_true", default=False)

        # questions_week = questions_graph + ["", "q800"
        #     ,"0-15-30-45-60-75-100__vaccin_now_later"
        #     ,"0-15-30-45-60-75-100__vaccin_now_later_mex"]

        return parser

    def get_cmd(self):
        """Return the cmd options"""

        cmd_options = self.get_parser().parse_args()
        logging.basicConfig(level=getattr(logging, cmd_options.debug.upper()))
        if cmd_options.ALL:
            cmd_options.csv = True
            cmd_options.maps = True
            cmd_options.reporting = True
            cmd_options.symptoms = True

        if cmd_options.no_csv:
            cmd_options.csv = False
        if cmd_options.no_symptoms:
            cmd_options.symptoms = False

        if cmd_options.cpus:
            try:
                cmd_options.cpus = int(cmd_options.cpus)
            except ValueError:
                sys.exit("cpu not an integer: {0}".format(cmd_options.cpus))
        else:
            cmd_options.cpus = 1

        if cmd_options.reload:
            webiap.config.DIAGRAMS["ini"]["reload"] = "True"

        return cmd_options

    def get_times(self):
        """Return the times"""
        times, errors = iap.utils.get_times(self.cmd_options.times)
        if "all" in errors:
            errors.remove("all")
            times["seasons"].append("all")

        if len(errors) > 0:
            print("Unrecognized times: {0}".format(", ".join(errors)))
        return times

    def main(self):
        """Create all figures"""
        # (Too many branches) pylint: disable=R0912
        # (Too many local vars) pylint: disable=R0914

        if self.cmd_options.cpus > 1:
            pool = tools.Pool(self.cmd_options.cpus)

            # output is written to stdout
            pool.add_listener(sys.stdout)

            def run(function, options):
                """Run the function parallel"""
                pool.apply_async(
                    stat_run, [function], dict(options))
        else:
            def run(function, options):
                """Run the function serial"""
                for result in stat_run(function, **options):
                    print(result)

        time0 = time.time()
        times = self.get_times()

        try:
            options = {"csv": self.cmd_options.csv,
                       "do_raise": self.cmd_options.do_raise}
            for (options["lang"],
                 options["country"], options["subset"],
                 options["season"],
                 options["size"]) in itertools.product(
                     self.parse("lang"),
                     times["countries"], self.parse("subset"),
                     times["seasons"], self.parse("size")):

                # if options["country"] in ["au", "br"]:
                #     webiap_old.config.DIAGRAMS["ini"]["plot_start"] = ""
                #     webiap_old.config.DIAGRAMS["ini"]["plot_end"] = ""
                #     webiap_old.config.DIAGRAMS["ini"]["plot_start_year"] = ""
                #     webiap_old.config.DIAGRAMS["ini"]["plot_end_year"] = ""
                # if options["season"] in ["2012/13"]:
                #     webiap_old.config.DIAGRAMS["ini"]["plot_end"] = "6/1"
                #     webiap_old.config.DIAGRAMS["ini"]["plot_end_year"] = "2013/6/1"
                # if options["country"] in ["br"]:
                #     webiap_old.config.DIAGRAMS["ini"]["min_value"] = 10
                #     webiap_old.config.DIAGRAMS["ini"]["min_participants"] = 10
                #     webiap_old.config.DIAGRAMS["ini"]["min_surveys"] = 1

                for source in self.parse("source"):
                    run(webiap.Europe, dict(options, source=source))

#                 if options["country"] not in webiap_old.config.DIAGRAMS[
#                       "params"]["inet"]:
#                     continue

                for casedef_id in (self.parse("casedef") +
                                   self.parse("syndrome")):
                    run(webiap.Casedef, dict(options, casedef_id=casedef_id))
                if self.cmd_options.reporting:
                    for casedef_id in self.parse("ili"):
                        run(webiap.Reporting,
                            dict(options, casedef_id=casedef_id))

                for activity in self.parse("activity"):
                    run(webiap.Activity, dict(options, activity=activity))

                for cutter in self.parse("histogram"):
                    run(webiap.HistCutter, dict(options, cutter=cutter))

                for options["casedef_id"] in self.parse("ili"):
                    for analysis in self.parse("analysis"):
                        run(webiap.Analysis,
                            dict(options, analysis=analysis))
                    for compare in self.parse("compare"):
                        run(webiap.Compare, dict(options, compare=compare))
                    for age in self.parse("age"):
                        run(webiap.Age, dict(options, age=age))

                    for cutter, average in itertools.product(
                            self.parse("cutter"), self.parse("average")):
                        run(webiap.IliCutter,
                            dict(options, cutter=cutter, average=average))

                    for control_id in self.parse("control"):
                        run(webiap.Control,
                            dict(options, control_id=control_id))
                del options["casedef_id"]

                if self.cmd_options.symptoms:
                    for casedef_id in (self.parse("syndrome") +
                                       self.parse("venn")):
                        run(webiap.Symptoms,
                            dict(options, casedef_id=casedef_id))

                for ili, cold in zip(self.parse("ili"), self.parse("cold")):
                    if (ili not in self.parse("syndrome") or
                            cold not in self.parse("syndrome")):
                        continue
                    run(webiap.Casedef,
                        dict(options, casedef_id="{0}@{1}".format(ili, cold)))

                for venn in self.parse("venn"):
                    for syndrome in self.parse(
                            "ili" if venn in ["s800_1", "s1120_1"] else
                            "cold" if venn == "s800_2" else
                            "allergy" if venn == "s800_3" else
                            "gastro" if venn == "s800_4" else
                            ""):
                        if syndrome == "corona" and venn != "s1120_1":
                            continue
                        if syndrome != "corona" and venn == "s1120_1":
                            continue
                        run(webiap.Casedef,
                            dict(options,
                                 casedef_id="{0}@{1}".format(venn, syndrome)))

            options = {"csv": self.cmd_options.csv,
                       "do_raise": self.cmd_options.do_raise}
            if (self.cmd_options.maps and
                    "nl" in times["countries"] and
                    "ilit" in self.parse("ili")):
                options["country"] = "nl"
                options["casedef_id"] = "ilit"
                options["lang"] = "en"
                options["min_incidence"] = 500
                options["max_incidence"] = 1500
                options["map_label"] = "ILI"
                for options["season"] in times["seasons"]:
                    run(webiap.Maps, options)

            if (self.cmd_options.maps and
                    "nl" in times["countries"] and
                    "corona" in self.parse("ili")):
                options["country"] = "nl"
                options["casedef_id"] = "corona"
                options["lang"] = "en"
                options["min_incidence"] = 1000
                options["max_incidence"] = 5000
                options["map_label"] = "<<casedef:corona>>"
                for options["season"] in times["seasons"]:
                    run(webiap.Maps, options)

            if (len(self.parse("week_cutter")) > 0 and
                    len(self.parse("week_casedef")) > 0):
                options["week_cutter_list"] = self.parse("week_cutter")
                options["week_casedef_list"] = self.parse("week_casedef")
                for options["country"] in times["countries"]:
                    for options["season"] in times["seasons"]:
                        run(webiap.Weeks, options)

            options = {"csv": self.cmd_options.csv,
                       "do_raise": self.cmd_options.do_raise}
            if "all" in times["seasons"] and self.cmd_options.csv:
                options["season"] = "all"
                for (options["country"], options["subset"]) \
                        in itertools.product(times["countries"],
                                             self.parse("subset")):

                    if (options["country"]
                            not in webiap.config.DIAGRAMS["params"]["inet"]):
                        continue
                    run(webiap.Csv, options)

        finally:
            if self.cmd_options.cpus > 1:
                pool.close()
                pool.join()

#                 while not pool.result_queue.empty():
#                     print(pool.result_queue.get(block=False))

        print("time = {0:.2f}".format(time.time() - time0))

if __name__ == "__main__":
    website = Website()
    website.main()
