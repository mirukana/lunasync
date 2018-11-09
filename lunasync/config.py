# Copyright 2018 miruka
# This file is part of lunasync, licensed under LGPLv3.

import csv
import shutil
from pathlib import Path
from typing import Optional

from appdirs import user_config_dir
from pkg_resources import resource_filename

from . import __about__

DEFAULT_FILE = resource_filename(__about__.__name__, "data/default_config.csv")
FILE         = f"%s/%s.csv" % (user_config_dir(__about__.__project_name__),
                               __about__.__pkg_name__)
FIELDS = ["tag_search", "filter", "labels", "booru"]
SUBS   = []

def reload(path: Optional[str] = None) -> None:
    path = Path(path or FILE).expanduser()

    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(DEFAULT_FILE, path)

    with open(path, "r") as file:
        SUBS.extend(list(
            csv.DictReader(
                (row for row in file if row and not row.startswith("#")),
                fieldnames = FIELDS
            )
        ))
