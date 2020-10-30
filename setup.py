#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2012 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Install script for influenzanet results website"""

import os
import glob

from distutils.core import setup


def data_include(install_root, local_root, exclude=None):
    """Include all files from a subdirectory"""
    if not exclude:
        exclude = []
    data_files = []
    for dirpath, _dirnames, fnames in os.walk(local_root):
        install_dir = os.path.normpath(os.path.join(install_root,
                os.path.relpath(dirpath, local_root)))
        files = [os.path.join(dirpath, fname) for fname in fnames
                if fname not in exclude]
        data_files.append((install_dir, files))
    return data_files


setup(name="influenzanet",
    version="20120226",
    description="Influenzanet Results Website",
    author="Sander van Noort",
    author_email="Sander.van.Noort@gmail.com",
    url="http://www.influenzanet.info/",
    packages=["webiap", "webiap/extra"],
    scripts=glob.glob("python/*.py"),
    license="AGPL v3",
    data_files=data_include("/var/www/influenzanet", "php")
            + data_include("/var/www/influenzanet", "config",
                    exclude=["local.ini", "users.csv"])
            + data_include("/var/www/influenzanet", "data")
            + data_include("/var/www/influenzanet/public", "public/eu")
            + data_include("/var/www/influenzanet/public", "public/images")
            + [("/var/www/influenzanet/public", ["public/index.php"])]
            + [("share/doc/influenzanet", ["LICENSE.txt"])]
            )
