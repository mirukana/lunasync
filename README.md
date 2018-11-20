# lunasync

[![PyPI downloads](http://pepy.tech/badge/lunasync)](
    http://pepy.tech/project/lunasync)
[![PyPI version](https://img.shields.io/pypi/v/lunasync.svg)](
    https://pypi.org/projects/lunasync)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/lunasync.svg)](
    https://pypi.python.org/pypi/lunasync)

Use [lunafind](https://github.com/mirukan/lunafind) to download
and keep in sync tag searches from Danbooru-based sites,
similar to Danbooru tag subscriptions/saved searches.

Searches are listed in a simple commented CSV file (see `--print-config-path`).  
Can be easily used with cron for automatic scheduling.

## Features

- Full and incremental syncs, incremental stops downloading after reaching the
  last post that was downloaded in a previous run
- Fast multithreaded downloads with lunafind, 8 downloads in parallel by default
- Can sync all or only searches with a specific labels
- Return the total number of downloaded posts

## Command line usage

After adding some searches to the config file,
simply doing `lunasync` will synchronize all searches in the current directory.  
A full sync will be taken for a search if this is the first time,
incremental else.
See `lunasync --help` for all options.

## Python usage

```python3
    import lunasync
    lunasync.sync()
```

See `help(lunasync.sync)` for parameters.

## Installation

Requires Python 3.6+ and pip (for automatic easy install).  
Tested on GNU/Linux only right now, but should work on other common OS.  
As root:

```sh
    pip3 install -U lunasync
```
