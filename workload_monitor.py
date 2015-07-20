#!/usr/bin/python
'''

Usage:
    workload_monitor.py CONFIG_FILENAME [-h | --help]
'''
import sys
from docopt import docopt
import setup_directories


def main(config_fn):
    ''''''
    config = read_config(config_fn)
    run_directory = setup_directories.main(config.workload_name)
    sys.stdout.write('Run directory created at %s\n' % run_directory)
    #start_monitors
    #run_workloads(config)
    #stop_monitors
    #tidy_results

#    return run_directory

class Config:
    def __init__(self):
        self.workload_name = None
        self.workload_description = None
        self.workload_command = None
        self.parameter1_name = "Iteration"
        self.parameter1_vals = []
        self.parameter1_factor = 1
        self.num_iterations = 1

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
    return config

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0')
    #print(arguments)
    main(arguments['CONFIG_FILENAME'])
