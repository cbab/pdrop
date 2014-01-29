pdrop
=====

`pdrop` is a Python script that uses [LTTng](http://www.lttng.org) to analyse packet drops occuring in the Linux kernel network stack.

The Linux kernel provides a tracepoint named `kfree_skb` that is called when [socket buffers](http://vger.kernel.org/~davem/skb.html) (skbs) are freed. By tracking these skbs deallocation, we are able to infer when packet drops occur in the Linux network stack. This method of tracking packet drops is currently limited. See the limitations section for more information.

`pdrop` track the `kfree_skb` events and provide useful information such as when and where a packet drop occured. 

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



## Limitations
