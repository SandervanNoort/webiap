#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2012 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Create access to downloadable data"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import os
import codecs
import crypt
import random
import sys  # pylint: disable=W0611
import getpass

import iap
import ifig

from ifig import tools

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_DIR = os.path.join(ROOT, "config")


class HtPass(object):
    """Class to add users to apache password file"""

    def __init__(self, passwd_fname):
        self.passwd_fname = passwd_fname
        tools.touch(passwd_fname)
        self.users = {}
        self.changed = False
        with tools.csvopen(self.passwd_fname, "r") as csvobj:
            reader = tools.ureader(csvobj, delimiter=":")
            for line in reader:
                user, passwd = line
                self.users[user] = passwd

    def get_hash(self, passwd):
        """Get a hash for passwd"""
        return crypt.crypt(passwd, self.salt())

    @staticmethod
    def salt():
        """Returns a string of 2 randome letters"""
        letters = 'abcdefghijklmnopqrstuvwxyz' \
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                  '0123456789/.'
        return random.choice(letters) + random.choice(letters)

    def add_user(self, user, passwd):
        """Add a user to the passwd file"""
        self.users[user] = self.get_hash(passwd)
        self.changed = True

    def remove_user(self, user):
        """Remove a user"""
        if user in self.users:
            del self.users[user]
            self.changed = True

    def write(self):
        """Write users to password file"""
        if not self.changed:
            return
        with open(self.passwd_fname, "w") as csvobj:
            writer = tools.uwriter(csvobj, delimiter=b":")
            for user, passwd in self.users.items():
                writer.writerow([user, passwd])
        self.changed = False

    def access(self, dirname, users):
        """Give access to a directory to users"""
        if not os.path.exists(dirname):
            print("ERROR: {0} does not exists".format(dirname))
            return

        with codecs.open(os.path.join(dirname, ".htaccess"),
                         "w", encoding="utf8") as fobj:
            if users is not None:
                fobj.write("AuthUserFile {0}\n".format(self.passwd_fname))
                fobj.write("AuthType Basic\n")
                fobj.write("AuthName \"Restricted access\"\n")
                fobj.write("Require user {0}\n".format(" ".join(users)))
            fobj.write("Options +Indexes\n")


class Data(object):
    """Class to create various data sets"""

    def __init__(self, htpass):
        iap.utils.period_available(None)
        self.countries = tools.SetList()
        self.seasons = tools.SetList()
        self.periods = list(iap.config.PERIODS["available"])
        self.htpass = htpass
        for period in self.periods:
            country, season = iap.utils.period_to_country_season(period)
            self.countries.append(country)
            self.seasons.append(season)
        self.permissions = self.get_permissions()

    @staticmethod
    def get_permissions():
        """Get users permissions"""
        fname = os.path.join(ifig.config.CONFIG_DIR, "users.csv")
        tools.touch(fname)
        perm = {}
        with open(fname, "r") as csvobj:
            reader = tools.ureader(csvobj)
            for line in reader:
                perm[line[0]] = line[1].split(":")
        return perm

    def get_users(self, country):
        """Return the users which have access to a country data"""
        users = []
        for user, countries in self.permissions.items():
            if "all" in countries or country in countries:
                users.append(user)
        return users

    def make_incidence(self):
        """Create links for the incidence data"""
        for country in self.countries:
            orig_name = os.path.join(ifig.config.DIRS["csv"],
                                     "{0}_all.csv".format(country))
            if not os.path.exists(orig_name):
                continue

            new_name = os.path.join(ifig.config.DIRS["download"], country,
                                    "incidence",
                                    "{0}_all.csv".format(country))
            tools.create_dir(new_name, remove=True)
            os.symlink(orig_name, new_name)

    def make_geo(self):
        """Create links for the geo data"""
        for period in self.periods:
            country = iap.utils.period_to_country_season(period)[0]
            orig_name = os.path.join(ifig.config.DIRS["csv"],
                                     "{0}_ilit_q100".format(country),
                                     "{0}.zip".format(period))
            if not os.path.exists(orig_name):
                continue

            new_name = os.path.join(
                ifig.config.DIRS["download"], country, "geo",
                "{0}.zip".format(period))
            tools.create_dir(new_name, remove=True)
            os.symlink(orig_name, new_name)
            self.htpass.access(os.path.dirname(new_name), None)

    def make_converted(self):
        """Create links for the geo data"""
        for period in self.periods:
            country, _season = iap.utils.period_to_country_season(period)
            orig_name = os.path.join(iap.config.LOCAL["dir"]["export"],
                                     "{0}.zip".format(period))
            if not os.path.exists(orig_name):
                continue

            new_name = os.path.join(ifig.config.DIRS["download"], country,
                                    "converted",
                                    "{0}.zip".format(period))
            tools.create_dir(new_name, remove=True)
            os.symlink(orig_name, new_name)
            self.htpass.access(os.path.dirname(new_name),
                               self.get_users(country))

    def make_orig(self):
        """Create links for the geo data"""
        questions = os.listdir(os.path.join(iap.config.LOCAL["dir"]["data"],
                                            "questions"))
        for period in self.periods:
            country, season = iap.utils.period_to_country_season(period)
            src = iap.utils.period_to_src(period)
            src2 = iap.utils.country_season_to_period("epi", season)
            orig_name = os.path.join(iap.config.LOCAL["dir"]["export"],
                                     "orig_{0}.zip".format(src))
            if not os.path.exists(orig_name):
                continue

            new_name = os.path.join(ifig.config.DIRS["download"], country,
                                    "orig",
                                    "orig_{0}.zip".format(src))
            tools.create_dir(new_name, remove=True)
            os.symlink(orig_name, new_name)

            for fname in questions:
                if fname.startswith(src) or fname.startswith(src2):
                    orig_name = os.path.join(
                        iap.config.LOCAL["dir"]["data"], "questions", fname)
                    new_name = os.path.join(
                        ifig.config.DIRS["download"], country, "orig", fname)
                    tools.create_dir(new_name, remove=True)
                    os.symlink(orig_name, new_name)

            self.htpass.access(os.path.dirname(new_name),
                               self.get_users(country))

    def create_users(self):
        """Create users/passwords from users.csv"""

        for user in self.permissions.keys():
            if user in self.htpass.users:
                continue
            password, password2 = 1, 2
            while password != password2:
                password = getpass.getpass("password for {0}:".format(user))
                password2 = getpass.getpass("Retype password:")
            if password != "":
                self.htpass.add_user(user, password)
        self.htpass.write()

if __name__ == "__main__":
    my_htpass = HtPass(os.path.join(ifig.config.CONFIG_DIR, "htpasswd.txt"))
    data = Data(my_htpass)
    data.create_users()
    data.make_incidence()
    data.make_converted()
    data.make_orig()
    data.make_geo()
