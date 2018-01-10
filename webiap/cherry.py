#!/usr/bin/env python
# -*-coding: utf-8-*-

# Copyright 2004-2013 Sander van Noort <Sander.van.Noort@gmail.com>
# Licensed under AGPLv3 (see LICENSE.txt)

"""Daemon to create plots via a webpage"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

import os
import codecs
import cherrypy
import io
import textwrap
import PIL

import iap.fig

from . import config, tools

MIME = {".png": "image/png",
        ".csv": "text/plain",
        ".ini": "text/plain",
        ".pdf": "application/pdf",
        ".txt": "text/plain",
        ".mp4": "video/mp4"}


class Cherry(object):
    """Class which generates images"""

    def __init__(self):
        self.output = io.StringIO()
        self.font = PIL.ImageFont.truetype(
            os.path.join(config.ROOT, "data", "mono.ttf"), size=16)

    def form_input(self, kwargs):
        """The INI form was submitted"""

        ext = (".csv" if kwargs.get("output") == "csv" else
               ".png")
        cherrypy.response.headers["Content-Type"] = MIME[ext][1]
        if "ini" not in kwargs:
            self.output_text("ERROR: no ini input", ext)
        else:
            ini = io.StringIO()
            ini.write(kwargs["ini"])
            self.convert(ini, None, ext)

    @cherrypy.expose
    def default(self, *args, **kwargs):
        """Default action"""
        self.output.seek(0)
        self.output.truncate()

        if len(args) > 1 and args[1] == "form":
            self.form_input(kwargs)
        elif len(args) > 2:
            ftype, lang = (
                args[1].split("_") if "_" in args[1] else
                (args[1], "en"))
            figname, ext = os.path.splitext(os.path.join(*args[2:]))
            ininame = os.path.join(
                config.get_dir("ini", lang), figname + ".ini")

            if ftype == "ini":
                self.ini_form(ininame)
            elif ftype in ["png", "csv"]:
                cherrypy.response.headers["Content-Type"] = MIME[ext]
                fname = os.path.join(
                    config.get_dir(ftype, lang), figname + ext)
                if (os.path.exists(fname) and
                        config.CONFIG["settings"]["cherry_cache"]):
                    # file exists / cached
                    with open(fname, "r", encoding="utf8") as fobj:
                        self.output.write(fobj.read())
                elif os.path.exists(ininame):
                    # file does not exists, but there is an ini
                    self.convert(ininame, fname, ext)
                else:
                    # neither an ini exists
                    self.output_text("No INI: {0}".format(args[-1]), ext)
            elif ftype in ["pdf", "map"]:
                fname = os.path.join(
                    config.get_dir(ftype, lang), figname + ext)
                if os.path.exists(fname):
                    cherrypy.response.headers["Content-Type"] = MIME[ext]
                    with open(fname, "r", encoding="utf8") as fobj:
                        self.output.write(fobj.read())
                else:
                    ext = ".txt"
                    cherrypy.response.headers["Content-Type"] = MIME[ext]
                    self.output_text("No file: {0}".format(figname), ".txt")
            else:
                ext = ".txt"
                cherrypy.response.headers["Content-Type"] = MIME[ext]
                self.output_text("Unknown extension: {0}".format(args[-1]),
                                 ext)
        else:
            ext = ".txt"
            cherrypy.response.headers["Content-Type"] = MIME[ext]
            self.output_text("Error: no arguments", ext)

        return self.output.getvalue()

    def ini_form(self, ininame):
        """Show an html form for ini files"""
        if os.path.exists(ininame):
            with codecs.open(ininame, "r", encoding="utf8") as fobj:
                ini = fobj.read()
        else:
            ini = ""
        self.output_text(
            """<html>
            <head>
            <title>Influenzanet INI generator</title>
            </head>
            <body>
            <form action='../form' method='get'>
            <textarea name='ini' cols='80' rows='20'>{ini}
            </textarea>
            <p>
            <input type='submit' name='output' value='image' />
            <input type='submit' name='output' value='csv' />
            </p>
            </form>
            </body>
            </html>
            """.format(ini=ini),  # ini_live=config.CONFIG["public"]["ini"]),
            ".html")

    def convert(self, ininame, fname, ext):
        """Convert an inifile"""

        try:
            myini = iap.Ini(ininame)
            if len(myini.datasets.keys()) == 0:
                self.output_text("No datasets: {0}".format(ininame), ext)
                return

            if ext == ".png":
                myfig = iap.fig.Fig(myini.settings)
                for plot_settings in myini.settings["plots"].values():
                    if not iap.fig.dia(myfig, plot_settings,
                                       myini.datasets).draw():
                        self.output_text("No data: {0}".format(ininame), ext)
                        return
                myfig.save(self.output)
            elif ext == ".csv":
                myexport = iap.Export(myini)
                myexport.write_csv(self.output)
        except iap.IAPError as error:
            self.output_text("Caught error: {0}".format(error), ext)
            return
        except Exception as error:
            self.output_text("Error: {0}".format(error), ext)
            return

        if fname:
            tools.create_dir(fname)
            with codecs.open(fname, "w", encoding="utf8") as fobj:
                fobj.write(self.output.getvalue())

    def output_text(self, text, ext):
        """Convert text to image"""

        if ext == ".png":
            image = PIL.Image.new("RGB", (350, 260), color="red")
            draw = PIL.ImageDraw.Draw(image)
            for i, text in enumerate(textwrap.wrap(text, width=30,
                                                   replace_whitespace=False)):
                draw.text((10, 10 + 20 * i), text, fill="black",
                          font=self.font)
            image.save(self.output, format="png")
        else:
            self.output.write(text)
