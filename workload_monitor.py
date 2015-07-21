#!/usr/bin/python
'''

Usage:
    workload_monitor.py CONFIG_FILENAME [-h | --help]
'''
import sys
import re
import socket
from docopt import docopt
import setup_directories


def main(config_fn):
    ''''''
    config = read_config(config_fn)
    run_directory = setup_directories.main(config.workload_name)
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

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0')
    #print(arguments)
    main(arguments['CONFIG_FILENAME'])
