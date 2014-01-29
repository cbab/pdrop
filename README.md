pdrop
=====

pdrop is a Python script that uses [LTTng](http://www.lttng.org) to analyse packet drops occuring in the Linux kernel network stack.

### Requirements

* Python 3
* LTTng toolchain >= 2.2
* Babeltrace git built with Python bindings support (Refer to Babeltrace README to see how bindings can be enabled)

#### Optional
* iproute2 (Provides the tc command)
* Network emulator module (sch_netem) (Required to emulate packet drop with the tc command, see [this](http://www.linuxfoundation.org/collaborate/workgroups/networking/netem) article for more information about netem)

### Usage

````
$ pdrop.py /path/to/trace
````

#### Sample output

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
* The third column, if present, indicates the function where the packet was dropped.

Note that the functions symbols are resolved using `/proc/kallsym` on the host where pdrop is runned.

#### Emulating packet drops


### Limitations
