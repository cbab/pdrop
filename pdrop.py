#!/usr/bin/env python3
#
# Copyright (C) 2014 - Christian Babeux <christian.babeux@efficios.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; only version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#

import sys
import argparse
import time

from babeltrace import *

# The get_kallsyms_table() and lookup_symbol() functions have been taken
# from perf "net_dropmonitor.py" script.
def get_kallsyms_table():
    kallsyms = []
    try:
        f = open("/proc/kallsyms", "r")
    except:
        return None

    for line in f:
        loc = int(line.split()[0], 16)
        name = line.split()[2]
        kallsyms.append((loc, name))

    kallsyms.sort()
    return kallsyms

def lookup_symbol(kallsyms, location):
    loc = int(location)
    # Invariant: kallsyms[i][0] <= loc for all 0 <= i <= start
    #            kallsyms[i][0] > loc for all end <= i < len(kallsyms)
    start, end = -1, len(kallsyms)

    while end != start + 1:
        pivot = (start + end) // 2
        if loc < kallsyms[pivot][0]:
            end = pivot
        else:
            start = pivot

    # Now (start == -1 or kallsyms[start][0] <= loc)
    # and (start == len(kallsyms) - 1 or loc < kallsyms[start + 1][0])
    if start >= 0:
        symloc, name = kallsyms[start]
        return (name, loc - symloc)
    else:
        return (None, 0)

def get_time_string(timestamp):
    # timestamp must be in ns since Epoch
    nsec_per_sec = 1000000000
    timestamp_s  = timestamp / nsec_per_sec
    timestamp_ns = timestamp % nsec_per_sec

    time_string  = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(timestamp_s))
    time_string += ".{0:0{width}}".format(timestamp_ns, width=9)
    return time_string

parser = argparse.ArgumentParser(description='Packet drop analysis.')
parser.add_argument('trace', metavar='trace', help='path to trace folder')
args = parser.parse_args()

traces = TraceCollection()
ret = traces.add_traces_recursive(args.trace, "ctf")

if ret is None:
    raise IOError("Error adding trace")

kallsyms = get_kallsyms_table()

if kallsyms is None:
    raise IOError("Error getting kallsyms")

for event in traces.events:
    if event.name == "skb_kfree":
        time_string      = get_time_string(event.timestamp)
        name             = event.name
        cpu_id           = event["cpu_id"]
        skbaddr          = hex(event["skbaddr"])
        location         = hex(event["location"])
        protocol         = event["protocol"]
        (symbol, offset) = lookup_symbol(kallsyms, event["location"])

        output = ""
        if symbol != None:
            output_format = "[{}] {} {}+{}"
            output = output_format.format(time_string, location, symbol, offset)
        else:
            output_format = "[{}] {}"
            output = output_format.format(time_string, location)

        print(output)
