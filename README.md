# eventlog
Minimalistic command line (curses) event logging tool in Python!

[![asciicast](https://asciinema.org/a/6vswglip07nqgkuken5fyew27.png)](https://asciinema.org/a/6vswglip07nqgkuken5fyew27)

Installation
------------
Easiest way to install eventlog is through pip.

	pip install git+https://github.com/jtorniainen/eventlog

Usage
-----
To start a logging session you only need to specify a filename for the resulting logfile.

	eventlog FILENAME

To resume an existing log you can use the `--append` option

	eventlog FILENAME --append

In the default mode the timestamps are taken using the system clock. You can also specify a NTP-server for more accurate timestamps with the `-ntp` option.

	eventlog FILENAME --ntp NTP_SERVER

For more information checkout `--help`

	eventlog --help

License
-------
MIT
