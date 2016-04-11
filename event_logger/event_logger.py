#!/usr/bin/env python3

# Jari Torniainen 2016
# Quantified Employee, Finnish Institute of Occupational Health
# MIT License (see LICENSE for details)

import curses
import datetime
import sys


def iso(timestamp):
    """ Convert timestamp to Colibri-ISO format """

    time_str = timestamp.isoformat()
    time_str = time_str.replace('-', '')
    time_str = time_str.replace(':', '')
    return time_str


def print_event_list(scr, events):
    """ Prints last 4 events to screen. """

    for line, event in enumerate(events[-4:]):
        time_str = '[{}]'.format(event[0].strftime('%H:%M:%S'))
        height, width = scr.getmaxyx()
        if len(event[1]) > width - 20:
            event_str = event[1][0:width - 20] + '...'
        else:
            event_str = event[1]
        scr.addstr(line + 3, 2, time_str, curses.A_BOLD)
        scr.addstr(line + 3, 3 + len(time_str), event_str)


def get_input(scr, timestamp):
    curses.echo()
    scr.clear()
    scr.addstr(2, 2, 'Enter new event:')
    scr.addstr(3, 2, '[{}]:'.format(timestamp))
    curses.curs_set(1)
    event_description = scr.getstr(5, 2, 160)
    curses.curs_set(0)
    curses.noecho()
    return event_description.decode('utf-8')


def main(scr, filename='testing.log'):

    # Write header for log-file (also removes existing entries)
    with open(filename, 'w') as file:
        file.write('Session started: {}\n'.format(datetime.datetime.now()))
        file.write('timestamp,event\n')

    running = True
    key = 0
    KEY_ENTER = 10
    KEY_Q = 113
    # KEY_ESC = ?

    events = []
    curses.curs_set(0)

    while running:

        scr.clear()
        # Draw current log
        scr.addstr(1, 2, 'EVENT LOGGER ({})'.format(filename))
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
            event_description = get_input(scr, timestamp)
            events.append((timestamp, event_description))
            # Write new event to file
            with open(filename, 'a') as file:
                file.write('{},{}\n'.format(iso(timestamp), event_description))

        elif key == KEY_Q:  # Quit
            running = False

        scr.refresh()


def run_from_cli():
    if len(sys.argv) == 2:
        curses.wrapper(main, sys.argv[1])
    else:
        print('event-logger needs filename as an argument!')

if __name__ == '__main__':
    run_from_cli()
