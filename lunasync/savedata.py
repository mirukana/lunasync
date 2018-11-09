# Copyright 2018 miruka
# This file is part of lunasync, licensed under LGPLv3.

import json
from pathlib import Path
from typing import Any, Dict, Optional

from appdirs import user_data_dir
from atomicfile import AtomicFile

from lunafind.utils import jsonify

from . import __about__

FILE = "%s/%s.csv" % (user_data_dir(__about__.__project_name__),
                      __about__.__pkg_name__)

DATA: Dict[str, Dict[str, Any]] = {}


def reload(path: Optional[str] = None) -> None:
    path = Path(path or FILE).expanduser()

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}")

    DATA.update(json.loads(path.read_text()))


def write(path: Optional[str] = None) -> None:
    path = Path(path or FILE).expanduser()

    with AtomicFile(path, "w") as file:
        file.write(jsonify(DATA, indent=4))
