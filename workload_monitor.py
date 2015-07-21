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
    config = read_config(config_fn)
    run_directory = setup_directories(config.workload_name)
    sys.stdout.write('Run directory created at %s\n' % run_directory)
    for parameter1 in config.parameter1_vals:
        run_id = create_run_id(config.parameter1_name, parameter1)
        #rc = execute_command(config.setup_command)
        launch_monitors(config, run_id)
    # run_workloads(config)
    # stop_monitors
    # tidy_results

#    return run_directory
def create_run_id(name, value):
    clean_name = re.sub(r'\W', '', name.replace(' ', '_'))
    clean_name = re.sub('_+', '_', clean_name).strip('_')
    return '%s=%s' % (clean_name, value)

def execute_command(cmd):
    if cmd:
        pass
    return -1
def launch_dstat(host, delay, run_id):
    fn = '/tmp/workload_monitor/%s.%s.dstat.csv' % (run_id, host.split('.')[0])
    remote_command = 'mkdir -p /tmp/workload_monitor/; '
    remote_command += 'dstat --time -v --net --output %s %d' % (fn, delay)
    print 'ssh %s "%s"' % (host, remote_command)
    # rc = os.system('ssh %s "%s"') % (host, remote_command)
    # assert rc==0
    return
def launch_monitors(config, run_id):
    for slave in config.slaves:
        launch_dstat(slave, config.measurement_delay_sec, run_id)
    return


class Config:
    def __init__(self):
        self.workload_name = None
        self.workload_description = None
        self.workload_command = None
        self.setup_command = None
        self.parameter1_name = "Iteration"
        self.parameter1_vals = ['']
        self.parameter1_factor = 1
        self.num_iterations = 1
        self.slaves = None
        self.run_ids = None
        self.measurement_delay_sec = 1

def read_config(config_filename):
    with open(config_filename, 'r') as fid:
        lines = fid.readlines()
    config = Config()
    for line in lines:
        line = line.strip()
        if len(line)<3 or line[0] == '#':
            pass
        else:
            argument = line.split()[0]
            value = ' '.join(line.split()[1:]).strip('\'"')
            setattr(config, argument, value)
    if not config.slaves:
        config.slaves = [socket.gethostname()]
    return config

def setup_directories(workload):
    '''
    Create these directories:
    ./rundir/[WORKLOAD_NAME]/[TIMESTAMP]/data/raw   # All config and raw data files end up here
    ./rundir/[WORKLOAD_NAME]/[TIMESTAMP]/data/final # Final (parsed) CSV files
    ./rundir/[WORKLOAD_NAME]/[TIMESTAMP]/scripts    # Measurement and analysis scripts
    And copy the html_source directory to:
    ./rundir/[WORKLOAD_NAME]/[TIMESTAMP]/html       # For interactive charts
    '''
    workload = workload.replace(' ', '_').upper()
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
    return run_directory

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0')
    #print(arguments)
    main(arguments['CONFIG_FILENAME'])
