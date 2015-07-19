#!/usr/bin/python
'''
Creates a set of directories for use by workload_monitor.py

./rundir/[WORKLOAD_NAME]/[TIMESTAMP]/data/raw   # All config and raw data files end up here
./rundir/[WORKLOAD_NAME]/[TIMESTAMP]/data/final # Final (parsed) CSV files
./rundir/[WORKLOAD_NAME]/[TIMESTAMP]/scripts    # Measurement and analysis scripts
./rundir/[WORKLOAD_NAME]/[TIMESTAMP]/html       # For interactive charts

Usage:
    setup_monitor.py WORKLOAD_NAME [-h | --help]
'''

import os
import sys
import shutil.copytree
from datetime import datetime
from docopt import docopt

def main(workload):
    '''Create run directory based on workload name and current timestamp'''
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
    directory = main(arguments['WORKLOAD_NAME'])
    sys.stdout.write(directory + '\n')
