#!/usr/bin/env python3
# -*-coding: utf-8-*-

"""Tools"""

from __future__ import (division, absolute_import, unicode_literals,
                        print_function)

# tools: *.py, ../bin/*.py

# pylint: disable=C0302

import collections
import re
import unicodedata
import six
import string
import configobj
import os
import shutil
import validate
import numpy
import sys
import io
import multiprocessing
import signal
import traceback
import types


class SetList(list):
    """Class which keeps all elements unique"""

    def __init__(self, init_list=None):
        list.__init__(self)
        if init_list is not None:
            for elem in init_list:
                self.append(elem)

    def __add__(self, list2):
        new = SetList(self)
        for elem in self._get_iter(list2):
            new.append(elem)
        return new

    @staticmethod
    def _get_iter(list2):
        """Return iterable list"""
        if not isinstance(list2, collections.Iterable):
            return [list2]
        else:
            return list2

    def __iadd__(self, list2):
        for elem in self._get_iter(list2):
            self.append(elem)
        return self

    def __sub__(self, list2):
        new = SetList(self)
        for elem in self._get_iter(list2):
            if elem in new:
                new.remove(elem)
        return new

    def __isub__(self, list2):
        for elem in self._get_iter(list2):
            if elem in self:
                self.remove(elem)
        return self

    def append(self, elem):
        if elem not in self:
            list.append(self, elem)

    def extend(self, list2):
        for elem in list2:
            self.append(elem)


def normalize(name):
    """Remove non-ascii strings"""

    # the input should by unicode
    if not isinstance(name, six.text_type):
        name = name.decode("utf8")

    # a unicode compatible with ascii
    output = unicodedata.normalize('NFKD', name)
    output = output.encode('ASCII', 'ignore').decode("ASCII")

    # only keep letters, numbers and " ", -, _
    output = "".join([c for c in output
                      if (ord(c) >= ord("a") and ord(c) <= ord("z")) or
                      (ord(c) >= ord("A") and ord(c) <= ord("Z")) or
                      (ord(c) >= ord("0") and ord(c) <= ord("9")) or
                      c in (" ", "-", "_")])
    output = re.sub("[ /]+", "_", output)
    output = re.sub("_+", "_", output)
    output = re.sub("_-_", "-", output)
    return output


class Cache(object):
    """Class which save output when called"""
    # (too few public methods) pylint: disable=R0903

    def __init__(self):
        self.output = None

    def __call__(self, output):
        self.output = output
        return output


def co_join(values):
    """Join a list to feed it to configobj"""
    if len(values) == 0:
        return ","
    elif len(values) == 1:
        return "{0},".format(values[0])
    else:
        return ", ".join(["{0}".format(elem) for elem in values])


class Format(string.Formatter):
    """Specific format class, with extras"""

    def __init__(self, format_string="", default=None):
        string.Formatter.__init__(self)
        self.format_string = format_string
        self.default = default

    def get_value(self, key, args, kwargs):
        """Get the value from the supplied arguments
           (or default)"""
        if self.default is not None:
            try:
                return string.Formatter.get_value(self, key, args, kwargs)
            except KeyError:
                return self.default
        else:
            return string.Formatter.get_value(self, key, args, kwargs)

    def format_field(self, value, spec):
        """Format the string (with configobj "co" syntax)"""
        cache = Cache()
        if spec == "co":
            # if cache(re.match("(.*)co$", spec)):
            value = co_join(value)
            spec = "s"
            # cache.output.group(1) + "s"
        elif cache(re.match(r"^sub(\d?)_?(.*)$", spec)):
            depth = (1 if cache.output.group(1) == "" else
                     int(cache.output.group(1)))
            value = "\n".join([
                "{0}{1} = {2}".format(depth * "    ", key, val)
                for key, val in value.items()])
            if cache.output.group(2) != "":
                value = (
                    depth * "[" + cache.output.group(2) + depth * "]" + "\n" +
                    value)
            spec = "s"
        return super(Format, self).format_field(value, spec)

    def format(self, extra=None, *args, **kwargs):
        """The format function with the extras"""
        if extra is not None:
            for key, value in extra.items():
                if key not in kwargs:
                    kwargs[key] = value
        return super(Format, self).format(self.format_string, *args, **kwargs)


def cobj_update(orig, new):
    """Recursive update"""
    for entry in new:
        if isinstance(new[entry], configobj.Section):
            cobj_update(orig[entry], new[entry])
        else:
            orig[entry] = new[entry]


def create_dir(fname, remove=False, is_dir=False, is_file=False):
    """If the directory for fname does not exists, create it"""

    if not isinstance(fname, six.string_types):
        print("cannot create_dir for {0}".format(fname))
        return

    dirname = os.path.dirname(fname)
    if is_file:
        dirname = dirname
    elif is_dir:
        dirname = fname
    elif os.path.splitext(fname)[1] == "":
        dirname = fname

    if os.path.exists(fname) and remove:
        if os.path.islink(fname) or os.path.isfile(fname):
            os.remove(fname)
        else:
            shutil.rmtree(fname)
    if dirname != "" and not os.path.exists(dirname):
        os.makedirs(dirname)


def cobj_check(settings, exception=None, copy=False):
    """Check for errors in config file"""

    if not exception:
        exception = Exception

    validator = validate.Validator()

    def numpy_array(val):
        """Define float list"""
        float_list = validator.functions["float_list"](val)
        return numpy.array(float_list)
    validator.functions["numpy_array"] = numpy_array

    results = settings.validate(validator, copy=copy, preserve_errors=True)
    if results is not True:
        output = "{0}: \n".format(
            settings.filename if settings.filename is not None else
            "configobj")
        for (section_list, key, error) in configobj.flatten_errors(
                settings, results):
            if key is not None:
                val = settings
                for section in section_list:
                    val = val[section]
                val = val[key] if key in val else "<EMPTY>"
                output += "   [{sections}], {key}='{val}' ({error})\n".format(
                    sections=', '.join(section_list),
                    key=key,
                    val=val,
                    error=error)
            else:
                output += "Missing section: {0}\n".format(
                    ", ".join(section_list))
        raise exception(output)


class Delayed(object):
    """Class which will delayed add variable/attributes"""
    # pylint: disable=R0903
    def __init__(self, name, init_func):
        self.module = sys.modules[name]
        self.init_func = init_func
        sys.modules[name] = self
        self.initializing = True

    def __getattr__(self, name):
        # call module.__init__ after import introspection is done
        if self.initializing and not name[:2] == '__' == name[-2:]:
            self.initializing = False
            self.init_func(self.module)
        return getattr(self.module, name)


if six.PY2:
    def csvopen(*args, **kwargs):
        """define open(), with binary for python2"""
        if len(args) > 1 and "b" not in args[1]:
            args = list(args)
            args[1] += "b"
        if "mode" in kwargs and "b" not in kwargs["mode"]:
            kwargs["mode"] += "b"
        return io.open(*args, **kwargs)
else:
    csvopen = io.open


def cprint(text):
    """Print with cpu number"""
    print("{0}: {1}".format(get_cpu(), text))


def get_cpu():
    """Return cpu number"""
    proc = multiprocessing.current_process()
    return int(proc.name.split("-")[1] if "-" in proc.name else "0")


class Pool(object):
    """self-written pool class which exits gracefully on keyboard exit"""

    def do_worker(self):
        """let a work go through the queue until it encounters None"""
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        cpu = get_cpu()
        while True:
            try:
                job = self.job_queue.get()
                if job is None:
                    self.result_in.send(None)
                    break
                function, args, kwargs = job
                result = function(*args, **kwargs)
                if isinstance(result, types.GeneratorType):
                    for sub_result in result:
                        self.result_in.send((sub_result, cpu))
                else:
                    self.result_in.send((result, cpu))
            except KeyboardInterrupt:
                pass
            except Exception as error:
                self.result_in.send(
                    (traceback.format_exc() if self.do_traceback else error,
                     cpu))

    def listener(self, output):
        """Monitor result queue and write to stdout"""

        count = 0
        while True:
            try:
                result = self.result_out.recv()
                if result is None:
                    count += 1
                    if count == self.processes:
                        break
                else:
                    result, cpu = result
                    output.write("{0} (cpu {1})\n".format(result, cpu))
                output.flush()
            except KeyboardInterrupt:
                pass

    def __init__(self, processes, do_traceback=False):
        """Main loop"""
        self.job_queue = multiprocessing.Queue()
        self.result_in, self.result_out = multiprocessing.Pipe()
        self.do_traceback = do_traceback
        self.processes = processes

        self.workers = []

        for _count in range(processes):
            worker = multiprocessing.Process(target=self.do_worker)
            worker.start()
            self.workers.append(worker)

    def add_listener(self, output):
        """Add a listener to the queue"""
        worker = multiprocessing.Process(target=self.listener,
                                         args=(output,))
        worker.start()
        self.workers.append(worker)

    def apply_async(self, function, args=None, kwargs=None):
        """Put job in the queue"""
        self.job_queue.put((function,
                            [] if args is None else args,
                            {} if kwargs is None else kwargs))

    def close(self):
        """Close the pool"""
        for _count in range(self.processes):
            self.job_queue.put(None)

    def join(self):
        """Wait for all workers to finish"""
        try:
            for worker in self.workers:
                worker.join()
        except KeyboardInterrupt:
            print("Gracefully exit due to keyboard interrupt")
            for worker in self.workers:
                worker.terminate()
                worker.join()
        except Exception:
            for worker in self.workers:
                worker.terminate()
                worker.join()

            raise
