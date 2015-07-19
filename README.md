# workload_monitor
Linux tool that:
 - launches a workload, or
 - launches a series of workloads while sweeping a parameter
 - records system data on one or more machines in a cluster, and
 - automatically generates an html page with interactive javascript charts.

Written in python, html, css and javascript.  

Setup
=====
- Install dstat via apt-get / yum
- Setup password-less ssh to localhost (and any other machines in your measurement cluster)
```
$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/user/.ssh/id_rsa):
Created directory '/home/user/.ssh'.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/user/.ssh/id_rsa.
Your public key has been saved in /home/user/.ssh/id_rsa.pub.
$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys   # repeat for other machines
$ ssh localhost
```

Quickstart
==========

Simple example
--------------
This tool works best when you create your own measurement script that is called
from the command line.  Here's a simple workload example script that first
writes a file, pauses 2 seconds, then reads the file again:
- [dd_write_then_read.sh](https://github.com/jschaub30/workload_monitor/blob/master/dd_write_then_read.sh).

After you create your command line script, create a configuration file
that describes the measurement. Here's the configuration file for this example:
- [example.conf](https://github.com/jschaub30/workload_monitor/blob/master/example.conf).

The workload is called and monitored by executing
`$ ./workload_monitor.py example.conf`


Example of sweeping a parameter
-------------------------------
The example workload script can be called by passing the block size to be used
for the file IO as the first parameter.

Here's the configuration file:
 - [example_sweep.conf](https://github.com/jschaub30/workload_monitor/blob/master/example_sweep.conf)

The workload is called and monitored by executing
`$ ./workload_monitor.py example_sweep.conf`


Example of monitoring multiple machines at once
-----------------------------------------------
Workloads that execute in a distributed environment can also be monitored.

Here's the configuration file:
 - [example_cluster.conf](https://github.com/jschaub30/workload_monitor/blob/master/example_cluster.conf)

The workload is called and monitored by executing
`$ ./workload_monitor.py example_cluster.conf`


Dependencies
============
This tool uses:
- [dstat](http://dag.wiee.rs/home-made/dstat/).  Install via apt-get/yum
- [docopt](https://github.com/docopt/docopt) for python command arguments (included)
- [C3js](http://c3js.org/) for javascript charts (included).
- [Dygraphs](http://dygraphs.com/) for javascript charts (included).
- [jquery-csv](https://code.google.com/p/jquery-csv/) for csv parsing (included).
- GNU-time /usr/bin/time
