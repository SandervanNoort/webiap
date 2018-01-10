#!/usr/bin/env python
# -*-coding: utf-8-*-

"""Download latest eiss data"""

from __future__ import division, absolute_import, unicode_literals

import iap
import sys  # pylint: disable=W0611

options = {"season": "2013/14"}

inistring = """
    [datasets]
        [[eiss]]
            source_measure = eiss_incidence
            country = {country}
            season = {season}
            casedef = ili
            casedef_id = ili
    """

for options["country"] in iap.utils.get_times(["ALL"])[0]["countries"]:
    period = iap.utils.country_season_to_period(options["country"],
                                                options["season"])
    iap.download.eiss_download(period, True)
    iap.download.eiss_fill(period)
    ini = iap.Ini(inistring.format(**options))
    data = iap.Data(ini.datasets["eiss"])
    datadict = data.get_datadict()
    print options["country"],
    if len(datadict.keys()) > 0:
        max_date = max(datadict.keys())
        print max_date, datadict[max_date]["eiss_incidence"]
    else:
        print "empty"
