#!/usr/bin/env python3
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
from webiap import tools
import iap



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


def parse_full(name, cmd_options):
    """Parse an argument as a comma seperated list"""

    if name in ["cold", "allergy", "gastro"]:
        return [name + ili[3:] for ili in parse_full("ili", cmd_options)]

    # a list, to not extend DIAGRAMS
    values = tools.SetList(getattr(cmd_options, name + "_list"))
    all_values = tools.SetList(
        webiap.config.DIAGRAMS["params"][name + "_list"])

#     elif name == "week_casedef_list":
#         all_values.extend(webiap.config.DIAGRAMS["params"]["ili_list"])
#         all_values.extend(webiap.config.DIAGRAMS["params"]["cold_list"])
#         all_values.extend(webiap.config.DIAGRAMS["params"]["venn_list"])
#         all_values.extend(
#             webiap.config.DIAGRAMS["params"]["casedef_list"])
#     elif name == "week_cutter_list":
#         all_values.extend(webiap.config.DIAGRAMS["params"]["cutter_list"])

    default = webiap.config.DIAGRAMS["params"].get(name + "_default", [])

    if values is None or len(values) == 0:
        values = all_values if cmd_options.ALL else default
    if "help" in values:
        sys.exit(
            "Possible values for {name}:\n   {values}".format(
                name=name, values=", ".join(all_values)))
    elif "ALL" in values:
        values = all_values
    elif "NONE" in values:
        values = []
    dif = set(values) - set(all_values)
    if not cmd_options.unknown and dif:
        sys.exit("Unknown {0}: {1}".format(name, ",".join(dif)))
    if name in BOOLEANS:
        values = [bool(int(val)) for val in values]

    if name == "syndrome":
        for syndrome in ["ili", "cold", "allergy", "gastro"]:
            if syndrome in values:
                values.remove(syndrome)
                values.extend(parse_full(syndrome, cmd_options))

    return values


def get_parser():
    """Return the commandline parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument(nargs="+", action="store", dest="times")

    parser.add_argument("-src", "--source_list", nargs="+", action="store")
    parser.add_argument("-cmp", "--compare_list", nargs="+", action="store")
    parser.add_argument("-cut", "--cutter_list", nargs="+", action="store")
    parser.add_argument("-his", "--histogram_list", nargs="+", action="store")
    parser.add_argument("-sub", "--subset_list", nargs="+", action="store")
    parser.add_argument("-avg", "--average_list", nargs="+", action="store")
    parser.add_argument("-ili", "--ili_list", nargs="+", action="store")
    parser.add_argument("-ven", "--venn_list", nargs="+", action="store")
    parser.add_argument("-syn", "--syndrome_list", nargs="+", action="store")
    parser.add_argument("-age", "--age_list", nargs="+", action="store")
    parser.add_argument("-act", "--activity_list", nargs="+", action="store")
    parser.add_argument("-ana", "--analysis_list", nargs="+", action="store")
    parser.add_argument("-con", "--control_list", nargs="+", action="store")
    parser.add_argument("-cas", "--casedef_list", nargs="+", action="store")
    parser.add_argument("-siz", "--size_list", nargs="+", action="store")
    parser.add_argument("-lan", "--lang_list", nargs="+", action="store")
    parser.add_argument("-wca", "--week_casedef_list", nargs="+",
                        action="store")
    parser.add_argument("-wcu", "--week_cutter_list", nargs="+",
                        action="store")

    parser.add_argument("-csv", "--csv", action="store_true")
    parser.add_argument("-nocsv", "--no-csv", action="store_true")

    parser.add_argument("-rep", "--reporting", action="store_true",
                        default=False)

    parser.add_argument("-sym", "--symptoms", action="store_true")
    parser.add_argument("-nosym", "--no-symptoms", action="store_true")

    parser.add_argument("-map", "--maps", action="store_true", default=False)
    parser.add_argument("-rel", "--reload", action="store_true", default=False)
    parser.add_argument("-deb", "--debug", action="store", dest="debug",
                        default="error")
    parser.add_argument("-unk", "--unknown", action="store_true",
                        default=False)
    parser.add_argument("-rai", "--raise", action="store_true",
                        default=False, dest="do_raise")

    parser.add_argument("-cpu", "--cpus", action="store")
    parser.add_argument("-ALL", action="store_true", default=False)

    # questions_week = questions_graph + ["", "q800"
    #     ,"0-15-30-45-60-75-100__vaccin_now_later"
    #     ,"0-15-30-45-60-75-100__vaccin_now_later_mex"]

    return parser


def get_cmd():
    """Return the cmd options"""

    cmd_options = get_parser().parse_args()
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


def get_times(cmd_options):
    """Return the times"""
    times, errors = iap.utils.get_times(cmd_options.times)
    if "all" in errors:
        errors.remove("all")
        times["seasons"].append("all")

    if errors:
        print("Unrecognized times: {0}".format(", ".join(errors)))
    return times


def get_run(cmd_options):
    """Get paralel or sequential run function"""

    if cmd_options.cpus > 1:
        pool = tools.Pool(cmd_options.cpus)

        # output is written to stdout
        pool.add_listener(sys.stdout)

        def run(function, options):
            """Run the function parallel"""
            pool.apply_async(
                stat_run, [function], dict(options))
    else:
        pool = None

        def run(function, options):
            """Run the function serial"""
            for result in stat_run(function, **options):
                print(result)
    return run, pool


def main():
    """Create all figures"""
    # (Too many branches) pylint: disable=R0912
    # (Too many local vars) pylint: disable=R0914

    cmd_options = get_cmd()

    def parse(val):
        """Use cmd_options by default"""
        return parse_full(val, cmd_options)

    run, pool = get_run(cmd_options)

    time0 = time.time()
    times = get_times(cmd_options)

    try:
        options = {"csv": cmd_options.csv,
                   "do_raise": cmd_options.do_raise}
        for (options["lang"],
             options["country"], options["subset"],
             options["season"],
             options["size"]) in itertools.product(
                 parse("lang"),
                 times["countries"], parse("subset"),
                 times["seasons"], parse("size")):

            # if options["country"] in ["au", "br"]:
            #     webiap.config.DIAGRAMS["ini"]["plot_start"] = ""
            #     webiap.config.DIAGRAMS["ini"]["plot_end"] = ""
            #     webiap.config.DIAGRAMS["ini"]["plot_start_year"] = ""
            #     webiap.config.DIAGRAMS["ini"]["plot_end_year"] = ""
            # if options["season"] in ["2012/13"]:
            #     webiap.config.DIAGRAMS["ini"]["plot_end"] = "6/1"
            #     webiap.config.DIAGRAMS["ini"]["plot_end_year"] \
            #       = "2013/6/1"
            # if options["country"] in ["br"]:
            #     webiap.config.DIAGRAMS["ini"]["min_value"] = 10
            #     webiap.config.DIAGRAMS["ini"]["min_participants"] = 10
            #     webiap.config.DIAGRAMS["ini"]["min_surveys"] = 1

            for options["source"] in parse("source"):
                run(webiap.Europe, options)

#                 if options["country"] not in webiap.config.DIAGRAMS[
#                       "params"]["inet"]:
#                     continue

            for options["casedef_id"] in (
                    parse("casedef") + parse("syndrome")):
                run(webiap.Casedef, options)
            if cmd_options.reporting:
                for options["casedef_id"] in parse("ili"):
                    run(webiap.Reporting, options)

            for options["activity"] in parse("activity"):
                run(webiap.Activity, options)

            for options["cutter"] in parse("histogram"):
                run(webiap.HistCutter, options)

            for options["casedef_id"] in parse("ili"):
                for options["analysis"] in parse("analysis"):
                    run(webiap.Analysis, options)
                for options["compare"] in parse("compare"):
                    run(webiap.Compare, options)
                for options["age"] in parse("age"):
                    run(webiap.Age, options)

                for options["cutter"], options["average"] in \
                        itertools.product(parse("cutter"), parse("average")):
                    run(webiap.IliCutter, options)

                for options["control_id"] in parse("control"):
                    run(webiap.Control, options)

            if cmd_options.symptoms:
                for options["casedef_id"] in parse("syndrome") + parse("venn"):
                    run(webiap.Symptoms, options)

            for ili, cold in zip(parse("ili"), parse("cold")):
                if (ili not in parse("syndrome") or
                        cold not in parse("syndrome")):
                    continue
                run(webiap.Casedef,
                    dict(options, casedef_id="{0}@{1}".format(ili, cold)))

            for venn in parse("venn"):
                for syndrome in parse(
                        "ili" if venn == "s800_1" else
                        "cold" if venn == "s800_2" else
                        "allergy" if venn == "s800_3" else
                        "gastro" if venn == "s800_4" else
                        ""):
                    run(webiap.Casedef,
                        dict(options,
                             casedef_id="{0}@{1}".format(venn, syndrome)))

        options = {"csv": cmd_options.csv,
                   "do_raise": cmd_options.do_raise}
        if (cmd_options.maps and
                "nl" in times["countries"] and
                "ilit" in parse("ili")):
            options["country"] = "nl"
            options["casedef_id"] = "ilit"
            options["lang"] = "en"
            for options["season"] in times["seasons"]:
                run(webiap.Maps, options)

        if parse("week_cutter") and parse("week_casedef"):
            options["week_cutter_list"] = parse("week_cutter")
            options["week_casedef_list"] = parse("week_casedef")
            for options["country"] in times["countries"]:
                for options["season"] in times["seasons"]:
                    run(webiap.Weeks, options)

        options = {"csv": cmd_options.csv,
                   "do_raise": cmd_options.do_raise}
        if "all" in times["seasons"] and cmd_options.csv:
            options["season"] = "all"
            for (options["country"], options["subset"]) \
                    in itertools.product(times["countries"],
                                         parse("subset")):

                if (options["country"]
                        not in webiap.config.DIAGRAMS["params"]["inet"]):
                    continue
                run(webiap.Csv, options)

    finally:
        if pool is not None:
            pool.close()
            pool.join()

#                 while not pool.result_queue.empty():
#                     print(pool.result_queue.get(block=False))

    print("time = {0:.2f}".format(time.time() - time0))

if __name__ == "__main__":
    main()
