pdrop
=====

`pdrop` is a Python script that uses [LTTng](http://www.lttng.org) to analyse packet drops occuring in the Linux kernel network stack.

Some Linux kernels provide a tracepoint named `kfree_skb` located in the function with the same name. This tracepoint is called when a [socket buffer](http://vger.kernel.org/~davem/skb.html) (skb) is deallocated. By tracking the socket buffers deallocation, we are able to infer when packet drops occur in the Linux kernel network stack. This method of tracking packet drops is currently limited. See the limitations section for more information.

`pdrop` tracks the `kfree_skb` events and provide useful information such as when and where a packet drop occured. 

## Requirements

* Python 3
* [LTTng](http://www.lttng.org) toolchain >= 2.2
* [Babeltrace](http://www.efficios.com/babeltrace) git master built with Python bindings support (Refer to Babeltrace [README](http://git.efficios.com/?p=babeltrace.git;a=blob_plain;f=README;hb=HEAD) to see how bindings can be enabled)

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
* The first column indicates the timestamp when the packet drop event occured.
* The second column indicates the address where the packet was dropped.
* The third column, if present, indicates the function+offset where the packet was dropped.

Note that the functions symbols are resolved using `/proc/kallsym` on the host where pdrop is runned.

### Emulating packet drops

The `trace.sh` script can be used to simulate packet drops. This script setups a tracing session using the lttng command-line tools (provided with the lttng-tools package) and enables the `kfree_skb` kernel event. It then proceeds with the simulation of packet drops with the help of the `tc` and the `sch_netem` network emulator module. Note that you must `modprobe sch_netem` before running this script.

When the script is done, you should have trace data available in the folder indicated. You can then proceed with the 
`pdrop` usage instructions above.

## Limitations
