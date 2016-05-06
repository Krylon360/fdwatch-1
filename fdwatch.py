#!/usr/bin/python
#! -*- coding: utf-8

from sys import argv, exit
from time import sleep
from os import path

"""
This file is part of fdwatch.

fdwatch is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

fdwatch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
"""


def humanize_bytes(bytes, precision=1):
    """Return a humanized string representation of a number of bytes.

    Assumes `from __future__ import division`.

    >>> humanize_bytes(1)
    '1 byte'
    >>> humanize_bytes(1024)
    '1.0 kB'
    >>> humanize_bytes(1024*123)
    '123.0 kB'
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    >>> humanize_bytes(1024*12342,2)
    '12.05 MB'
    >>> humanize_bytes(1024*1234,2)
    '1.21 MB'
    >>> humanize_bytes(1024*1234*1111,2)
    '1.31 GB'
    >>> humanize_bytes(1024*1234*1111,1)
    '1.3 GB'
    """
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)


def elapsed_time(seconds, suffixes=['y', 'w', 'd', 'h', 'm', 's'], add_s=False,
                 separator=' '):
        """
        Takes an amount of seconds and turns it into a human-readable amount
        of time.
        """
        # the formatted time string to be returned
        time = []

        # the pieces of time to iterate over (days, hours, minutes, etc)
        # - the first piece in each tuple is the suffix (d, h, w)
        # - the second piece is the length in seconds (a day is 60s*60m*24h)
        parts = [(suffixes[0], 60 * 60 * 24 * 7 * 52),
                 (suffixes[1], 60 * 60 * 24 * 7),
                 (suffixes[2], 60 * 60 * 24),
                 (suffixes[3], 60 * 60),
                 (suffixes[4], 60),
                 (suffixes[5], 1)]

        # for each time piece, grab the value and remaining seconds, and add it
        # to the time string
        for suffix, length in parts:
                value = int(seconds / length)
                if value > 0:
                        seconds = seconds % length
                        time.append('%d%s' % (value,
                                   (suffix, (suffix, suffix + 's')[value > 1])[
                                       add_s]))
                if seconds < 1:
                        break

        return separator.join(time)

if __name__ == "__main__":
    if len(argv) != 3:
        exit("Usage: %s <PID> <FD_NUMBER>" % (argv[0]))
    pid = argv[1]
    fdno = argv[2]

    while 1:
        fd = open("/proc/%s/fdinfo/%s" % (pid, fdno))
        old_stat = float(fd.readline()[5:].strip("\n"))
        size = path.getsize("/proc/%s/fd/%s" % (pid, fdno))
        sleep(1)
        fd = open("/proc/%s/fdinfo/%s" % (pid, fdno))
        new_stat = float(fd.readline()[5:].strip("\n"))

        percent = "%0.2f%%" % (float(old_stat/size)*100)
        delta = new_stat-old_stat
        if delta == 0:
            continue
        #speed = "%0.2f MiB/s" % (delta/1024**2)
        speed = "%s/s" % humanize_bytes(delta)
        eta = "ETA=%s" % elapsed_time(separator=' ',
                                      seconds=int((size - new_stat)/delta))
        print("%s, %s, ETA: %s" % (percent, speed, eta))
