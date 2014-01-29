#!/bin/bash
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

EVENTS=(skb_kfree)
SESSION="packet_drop"
TRACE_PATH=$(mktemp -d)

echo "Trace path: ${TRACE_PATH}"

lttng create --output ${TRACE_PATH} ${SESSION}

for EVENT in ${EVENTS[@]};
do
    lttng enable-event --session ${SESSION} --kernel ${EVENT}
done

# Make sure that the "sch_netem" module is loaded before running this script.
tc qdisc add dev eth0 root netem loss 10%

lttng start
sleep 60
lttng stop

tc qdisc del dev eth0 root

lttng destroy ${SESSION}
