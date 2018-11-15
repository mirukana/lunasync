# Copyright 2018 miruka
# This file is part of lunasync, licensed under LGPLv3.

r"""Usage: lunasync [LABEL]... [options]

Keep downloaded booru searches up-to-date, similar to Danbooru subscriptions.

Subscriptions are defined in the config file (see `--print-config-path`),
and will be downloaded/updated using `lunafind`.
The number of posts downloaded will be output on stdout.

Arguments:
  LABEL
    If label arguments are passed, only synchronize subscriptions that have
    at least one of the indicated label.
    This can be useful for e.g. scheduling certain subscription syncs
    with cron at different intervals.
    With no argument, synchronize everything.

Options:
  -f, --force
    Force a complete re-check for subscriptions.
    Without this, the sync will stop upon reaching the most recently
    downloaded post of previous syncs (if there were any).

  -d DIR, --local-dir DIR
    Path to the directory where to download posts.
    If unspecified, the current directory (`.`) is used.

  -q, --quiet-skip
    Do not warn when skipping download of already existing files.

  -o, --overwrite
    Force download and overwrite any files that already exist.


  --config PATH
    Use `PATH` as configuration file instead of the default location.

  --print-config-path
    Show the configuration file path.
    If the file doesn't exist, a default one is automatically copied.

  -h, --help
    Show this help.

  -V, --version
    Show the program version."""

import sys
import time
from typing import List, Optional

import docopt

import lunafind

from . import __about__, config, sync


def main(argv: Optional[List[str]] = None) -> None:
    argv = argv if argv is not None else sys.argv[1:]

    try:
        args = docopt.docopt(
            __doc__, help=False, argv=argv, version=__about__.__version__
        )
    except docopt.DocoptExit:
        if len(sys.argv) > 1:
            print(lunafind.TERM.red("Invalid command syntax, check help:\n"))

        lunafind.utils.print_colored_help(__doc__, exit_code=10)

    if args["--config"]:
        config.FILE = args["--config"]
        config.reload()

    if args["--help"]:
        lunafind.utils.print_colored_help(__doc__)

    if args["--print-config-path"]:
        print(config.FILE)
        sys.exit()

    downloaded = sync(
        only_for_labels = args["LABEL"],
        force_full      = args["--force"],
        base_dir        = args["--local-dir"] or ".",
        overwrite       = args["--overwrite"],
        warn            = not args["--quiet-skip"]
    )

    time.sleep(0.2)  # Other threads might manage to print after this else
    print(downloaded)
