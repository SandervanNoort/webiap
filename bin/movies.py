#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2012 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Create all the results for web page"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import subprocess
import os
import shutil
import sys

import webiap
from webiap import tools

FRAMERATE = 1
BITRATE = 1800
EXT = "mp4"


def get_map_dirs():
    """Get all the dirs which contain a map"""
    map_dir = webiap.DIRS["map"]
    results_dir = os.path.dirname(map_dir)
    basename = os.path.basename(map_dir)
    for map_dir_lang in os.listdir(results_dir):
        if map_dir_lang.startswith(basename):
            for country_season in os.listdir(os.path.join(results_dir,
                                                          map_dir_lang)):
                yield os.path.join(results_dir, map_dir_lang, country_season)


def main():
    """Main loop"""

    for map_dir in get_map_dirs():
        # create subdir movie which stores temp files
        movie_dir = os.path.join(map_dir, "movie")
        tools.create_dir(movie_dir, remove=True)

        # put symlinks in the folder "movie"
        number = 0
        for image in sorted(os.listdir(map_dir)):
            if image.endswith("png"):
                os.link(os.path.join(map_dir, image),
                        os.path.join(movie_dir, "{0:03d}.png".format(number)))
                number += 1
        if number == 0:
            continue

        # make the movie
        moviename = os.path.join(map_dir, "movie.{0}".format(EXT))
        if os.path.exists(moviename):
            os.remove(moviename)
        print("Creating", moviename)
        cmd = ("ffmpeg -r {frame_rate} -b {bit_rate}" +
               " -i {movie_dir}/%03d{ext} {moviename}").format(
            frame_rate=FRAMERATE,
            bit_rate=BITRATE,
            movie_dir=movie_dir,
            ext=".png",
            moviename=moviename)
        try:
            subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            print(cmd)
            print(error)
            sys.exit()
        shutil.rmtree(movie_dir)

if __name__ == "__main__":
    main()
