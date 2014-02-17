pdrop
=====

`pdrop` is a Python script that uses [LTTng](http://www.lttng.org) to analyze packet drops occurring in the Linux kernel network stack.

Some Linux kernels provide a tracepoint named `kfree_skb` located in the function with the same name. This tracepoint is called when a [socket buffer](http://vger.kernel.org/~davem/skb.html) (skb) is deallocated. By tracking the socket buffers deallocation, we are able to infer when packet drops occur in the Linux kernel network stack. This method of tracking packet drops is currently limited. See the limitations section for more information.

`pdrop` tracks the `kfree_skb` events and provides useful information such as when and where a packet drop occurred. 

## Requirements

* Python 3
* [LTTng](http://www.lttng.org) toolchain >= 2.2
* [Babeltrace](http://www.efficios.com/babeltrace) git master built with Python bindings support (refer to Babeltrace [README](http://git.efficios.com/?p=babeltrace.git;a=blob_plain;f=README;hb=HEAD) to see how bindings can be enabled)

### Optional
* [iproute2](http://www.linuxfoundation.org/collaborate/workgroups/networking/iproute2) (Provides the tc command)
* [Network emulator module](http://www.linuxfoundation.org/collaborate/workgroups/networking/netem) (sch_netem) (Required to emulate packet loss with the tc command)

## Usage

````
$ pdrop.py /path/to/trace
````

### Sample output

````
$ pdrop.py trace/
[2014-01-27 17:52:34.544754084] 0xffffffff81414cd0 tcp_v4_do_rcv+112
[2014-01-27 17:52:34.544781010] 0xffffffff814171b8 tcp_v4_rcv+424
[2014-01-27 17:52:54.544989518] 0xffffffff81414cd0 tcp_v4_do_rcv+112
[2014-01-27 17:52:54.545000818] 0xffffffff814171b8 tcp_v4_rcv+424
[2014-01-27 17:53:09.867714636] 0xffffffff81414cd0 tcp_v4_do_rcv+112
[2014-01-27 17:53:09.867831349] 0xffffffff814171b8 tcp_v4_rcv+424
[2014-01-27 17:53:10.542946516] 0xffffffff81414cd0 tcp_v4_do_rcv+112
[2014-01-27 17:53:10.542955301] 0xffffffff814171b8 tcp_v4_rcv+424
[2014-01-27 17:53:14.552876436] 0xffffffff81414cd0 tcp_v4_do_rcv+112
[2014-01-27 17:53:14.552884595] 0xffffffff814171b8 tcp_v4_rcv+424
````
* The first column indicates the timestamp when the packet drop event occurred.
* The second column indicates the address where the packet was dropped.
* The third column, if present, indicates the function+offset where the packet was dropped.

Note that the functions symbols are resolved using `/proc/kallsym` on the host where pdrop is runned.

### Emulating packet drops

The `trace.sh` script can be used to simulate packet drops. This script setups a tracing session using the lttng command-line tools (provided with the lttng-tools package) and enables the `skb_kfree` kernel event. It then proceeds with the simulation of packet drops with the help of the `tc` and the `sch_netem` network emulator module. Note that you must `modprobe sch_netem` before running this script.

When the script is done, you should have trace data available in the folder indicated. You can then proceed with the 
`pdrop` usage instructions above.

## Limitations

The methodology used by `pdrop` to detect packet drops in the Linux kernel network stack has some limitations. It is often the case that a reported packet drop is a perfectly normal situation of deallocations on networking cleanup/teardown code paths. Thus this tool might report false-positive situations. The current way of detecting packet drop rely on the "side-effect" of deallocation of a socket buffer in the `kfree_skb()` function. The commit ["ead2ceb0ec9f85cff19c43b5cdb2f8a054484431"][dropwatch commit] in the Linux kernel changed the semantic of the `kfree_skb()` and introduced a replacement function `consume_skb()` that should be used in non-packet drop deallocation situation. Normal socket buffer teardown/cleanup paths _should_  use `consume_skb()`. This is often not the [case][false-positive]. Thus we often see false-positive. All the tools (SystemTAP [dropwatch.stp][dropwatch.stp], Perf [net_dropmonitor][net_dropmonitor.py] and [dropwatch][dropwatch]) using the `kfree_skb` tracepoint mechanism all suffer from the same limitation.

Moreover, some code paths where network packets are dropped (e.g.: failure to allocate a skb) might not even get reported because they are not calling `kfree_skb()`.

[dropwatch commit]: https://git.kernel.org/cgit/linux/kernel/git/stable/linux-stable.git/commit/?id=ead2ceb0ec9f85cff19c43b5cdb2f8a054484431
[false-positive]: https://git.kernel.org/cgit/linux/kernel/git/stable/linux-stable.git/commit/?id=5d0ba55b6486f58cc890918d7167063d83f7fbb4
[dropwatch.stp]: https://sourceware.org/systemtap/SystemTap_Beginners_Guide/useful-systemtap-scripts.html#dropwatch
[net_dropmonitor.py]: https://git.kernel.org/cgit/linux/kernel/git/stable/linux-stable.git/plain/tools/perf/scripts/python/net_dropmonitor.py
[dropwatch]: https://fedorahosted.org/dropwatch/
