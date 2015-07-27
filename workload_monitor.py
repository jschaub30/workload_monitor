#!/usr/bin/python
'''

Usage:
    workload_monitor.py CONFIG_FILENAME [-h | --help]
'''
import sys
import os
import re
import socket
from docopt import docopt
import shutil
from datetime import datetime


def main(config_fn):
    ''''''
    # TODO: Do I need to pass around config?
    config = read_config(config_fn)
    setup_directories(config)
    sys.stdout.write('Run directory created at %s\n' % config.run_directory)
    for parameter1 in config.parameter1_vals:
        for iteration in xrange(int(config.num_iterations)):
            create_run_id(config, parameter1, iteration)
            execute_local_command(config.setup_command)
            start_monitors(config)
            # Now run the workload
            val = parameter1
            if config.parameter1_factor:
                try:
                    val = float(parameter1) * int(config.parameter1_factor)
                    val = str(val).rstrip('.0')
                except ValueError:
                    msg = 'Problem multiplying parameter (%s) by factor (%s)' % (
                          parameter1, config.parameter1_factor)
                    msg += '\nContinuing...\n'
                    sys.stderr.write(msg)
            command = '%s %s' % (config.workload_command, val)
            execute_local_command(command)
            stop_monitors(config)
            # tidy_results

#    return run_directory


def create_run_id(config, value, iteration):
    name = config.parameter1_name
    clean_name = re.sub(r'\W', '', name.replace(' ', '_'))
    clean_name = re.sub('_+', '_', clean_name).strip('_')
    run_id = '%s=%s.%d' % (clean_name, value, iteration)
    if not config.run_ids:
        config.run_ids = [run_id]
    else:
        config.run_ids.append(run_id)
    return


def execute_local_command(cmd):
    '''Execute a command on the local machine'''
    if cmd:
        #rc = os.system(cmd)
        print 'Now executing local command: ' + cmd
        # assert rc==0
    return


def launch_dstat(host, delay, run_id):
    '''Launch the dstat monitoring utility on host'''
    fn = '/tmp/workload_monitor/%s.%s.dstat.csv' % (run_id, host.split('.')[0])
    remote_command = 'mkdir -p /tmp/workload_monitor/; '
    remote_command += 'dstat --time -v --net --output %s %s' % (fn, delay)
    print 'ssh %s "%s"' % (host, remote_command)
    # rc = os.system('ssh %s "%s"') % (host, remote_command)
    # assert rc==0
    return


def start_monitors(config):
    '''Launch all system monitors on all machines in the cluster'''
    for slave in config.slaves:
        launch_dstat(slave, config.measurement_delay_sec, config.run_ids[-1])
    return


def kill_dstat(host):
    '''Kill the dstat monitoring utility on host'''
    remote_command = 'killall dstat'
    print 'ssh %s "%s"' % (host, remote_command)
    # rc = os.system('ssh %s "%s"') % (host, remote_command)
    # assert rc==0
    return


def stop_monitors(config):
    '''
    Stop all system monitors on all machines in the cluster, then
    copies output files from each slave to run directory
    '''
    for slave in config.slaves:
        kill_dstat(slave)
        command = 'scp %s:/tmp/workload_monitor/%s/* %s/data/raw/.' % (
            slave, config.run_directory, config.run_directory)
        print 'Executing: ' + command
        # rc = os.system('ssh %s "%s"') % (host, remote_command)
        # assert rc==0

    return


class Config:

    def __init__(self):
        self.workload_name = None
        self.workload_description = None
        self.workload_command = None
        self.setup_command = None
        self.parameter1_name = "Iteration"
        self.parameter1_vals = ['']
        self.parameter1_factor = None
        self.num_iterations = '1'
        self.slaves = None
        self.run_ids = None
        self.measurement_delay_sec = '1'
        self.run_directory = None
        self.run_ids = None


def read_config(config_filename):
    with open(config_filename, 'r') as fid:
        lines = fid.readlines()
    config = Config()
    for line in lines:
        line = line.strip().split('#')[0]
        if len(line) < 3 or line[0] == '#':
            pass
        else:
            argument = line.split()[0]
            value = ' '.join(line.split()[1:]).strip('\'"')
            if argument == 'parameter1_vals':
                setattr(config, argument, [value])
            else:
                setattr(config, argument, value)
    if not config.slaves:
        config.slaves = [socket.gethostname()]
    return config


def setup_directories(config):
    '''
    Create these directories:
    ./rundir/[WORKLOAD_NAME]/[TIMESTAMP]/data/raw   # Raw data files
    ./rundir/[WORKLOAD_NAME]/[TIMESTAMP]/data/final # Final (parsed) CSV files
    ./rundir/[WORKLOAD_NAME]/[TIMESTAMP]/scripts    # Measurenment and analysis scripts
    And copy the html_source directory to:
    ./rundir/[WORKLOAD_NAME]/[TIMESTAMP]/html       # For interactive charts
    '''
    workload = config.workload_name.replace(' ', '_').upper()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_directory = os.path.join('rundir', workload, timestamp)
    for sub_directory in ['data/raw', 'data/final', 'scripts']:
        full_path = os.path.join(run_directory, timestamp, sub_directory)
        os.makedirs(full_path)

    # Now copy html directory, if one exists
    if os.path.exists('html_source'):
        shutil.copytree('html_source',
                        os.path.join(run_directory, timestamp, 'html'))

    # Create 'latest' symbolic link
    os.chdir(os.path.join('rundir', workload))
    try:
        os.unlink('latest')
    except OSError:
        pass
    os.symlink(timestamp, 'latest')
    config.run_directory = run_directory
    return

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0')
    # print(arguments)
    main(arguments['CONFIG_FILENAME'])
