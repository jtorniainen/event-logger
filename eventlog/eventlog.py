#!/usr/bin/env python3

# Jari Torniainen 2016
# Quantified Employee, Finnish Institute of Occupational Health
# MIT License (see LICENSE for details)

import curses
import datetime
import ntplib
import argparse
import os
import sys


def iso(timestamp):
    """ Convert timestamp to Colibri-ISO format

    Args:
        timestamp: datetime timestamp

    Returns:
        time_str: ISO-formatted timestamp string
    """

    time_str = timestamp.isoformat()
    time_str = time_str.replace('-', '')
    time_str = time_str.replace(':', '')
    return time_str


def print_event_list(scr, events):
    """ Prints the last four events to screen.

    Args:
        scr: curses screen
        events: list of logged events
    """

    for line, event in enumerate(events[-4:]):
        time_str = '[{}]'.format(event[0].strftime('%H:%M:%S'))
        height, width = scr.getmaxyx()
        if len(event[1]) > width - 20:
            event_str = event[1][0:width - 20] + '...'
        else:
            event_str = event[1]
        scr.addstr(line + 3, 2, time_str, curses.A_BOLD)
        scr.addstr(line + 3, 3 + len(time_str), event_str)


def add_entry(scr, timestamp):
    curses.echo()
    scr.clear()
    scr.addstr(2, 2, 'Enter new event:')
    scr.addstr(3, 2, '[{}]:'.format(timestamp))
    curses.curs_set(1)
    event_description = scr.getstr(5, 2, 160)
    curses.curs_set(0)
    curses.noecho()
    return event_description.decode('utf-8')


def main(scr, filename, ntp=False, append=False):
    """ eventlog main

    Args:
        scr: curses screen (from wrapper)
        filename: output filename
        ntp: ntp server address (optional)
        append: append to existing file (optional)
    """

    running = True
    start_time = datetime.datetime.now()
    key = 0
    KEY_ENTER = 10
    KEY_Q = 113

    events = []
    curses.curs_set(0)

    offset = 0

    if ntp:
        client = ntplib.NTPClient()
        request = client.request(ntp)
        offset = request.offset

    if not append:
        # Write header for log-file (also removes existing entries)
        with open(filename, 'w') as file:
            file.write('# {}\n'.format(start_time.strftime('%D-%T')))
            file.write('# NTP={} offset={:0.5f}\n'.format(ntp, offset))
            file.write('# timestamp,event\n')

    while running:

        scr.clear()
        # Draw current log
        scr.addstr(1, 2, 'EVENTLOG ({})'.format(filename))
        print_event_list(scr, events)
        scr.addstr(9, 2, 'ENTER', curses.A_BOLD)
        scr.addstr(9, 8, 'Add event')
        scr.addstr(10, 2, 'Q', curses.A_BOLD)
        scr.addstr(10, 8, 'Quit')

        # Wait for input
        key = scr.getch()
        # Process input
        if key == KEY_ENTER:  # Add entry
            # Get as accurate time stamp as possible
            timestamp = datetime.datetime.now()
            timestamp += datetime.timedelta(seconds=offset)
            event_description = add_entry(scr, timestamp)
            events.append((timestamp, event_description))
            # Write new event to file
            with open(filename, 'a') as file:
                file.write('{},{}\n'.format(iso(timestamp), event_description))
        elif key == KEY_Q:  # Quit
            running = False
        scr.refresh()


def run_from_cli():
    """ Run eventlog from the command line. """

    if sys.version_info < (3, 0):
        input = raw_input

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='filename for the logfile')
    parser.add_argument('-n', '--ntp', help='specify the NTP server', type=str)
    parser.add_argument('-a', '--append',
                        help='append to an existing file',
                        action='store_true')
    arguments = parser.parse_args()

    # Check if the output file already exists
    if not arguments.append and os.path.isfile(arguments.filename):
        if input('Warning: File exists, overwrite? [y/n]: ') != 'y':
            return

    # Check if were are trying to append to a non-existing file
    if arguments.append and not os.path.isfile(arguments.filename):
        print('Error: Trying to append to a non-existing file!')
        return

    curses.wrapper(main, arguments.filename, arguments.ntp, arguments.append)

if __name__ == '__main__':
    run_from_cli()
