# pupstat

Service status and uptime logging. Works with any service that listens on a 
port.

Outputs json with percentage uptime, and current state.

## Installation

First follow the configuration instructions, then run `make && sudo make 
install`.

### Configuration

To configure edit the dictionary at the top of `pupstat.py` to match the
services you want to monitor.

